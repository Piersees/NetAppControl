// dllmain.cpp : Définit le point d'entrée pour l'application DLL.
#include "stdafx.h"
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <windows.h>
#include <stdio.h>
#include <winsock2.h>
#include <stdlib.h>
#include <string>

// Need to link with Ws2_32.lib
#pragma comment(lib, "ws2_32.lib")

BOOL WriteMemory(FARPROC fpFunc, const BYTE * b, SIZE_T size);
VOID HookConnect(VOID);
VOID HookBind(VOID);

FARPROC fpConnect;
BYTE bSavedByte;

FARPROC fpBind;
BYTE bSavedByteBind;
char* ip;



void getIp() {

	HANDLE hPipe;
	DWORD dwRead;

	char szTest[256];
	sprintf_s(szTest, "\\\\.\\pipe\\%d", GetCurrentProcessId());

	hPipe = CreateFileA(
		szTest,   // pipe name 
		GENERIC_READ,
		0,              // no sharing 
		NULL,           // default security attributes
		OPEN_EXISTING,  // opens existing pipe 
		0,              // default attributes 
		NULL);          // no template file 

	DWORD numBytesRead = 0;
	BOOL result = false;
	int count = 0;

	while ((!result) && (count<10))
	{
		DWORD bytesAvail = 0;
		while ((bytesAvail == 0) && (count<10))
		{
			count += 1;
			PeekNamedPipe(hPipe, NULL, 0, NULL, &bytesAvail, NULL);
			Sleep(100);
		}
		
		char* buffer = (char*)malloc(bytesAvail-4);

		result = ReadFile(
			hPipe,    // pipe handle 
			buffer,    // buffer to receive reply 
			bytesAvail,  // size of buffer 
			&numBytesRead,  // number of bytes read 
			NULL);    // not overlapped 

		if (result) {
			ip = buffer;
			MessageBoxA(NULL, ip, "DLL Injected",
				MB_OK);

		}
	}

	return;
}

int MyBind(SOCKET s, sockaddr *name, int len) {

	// bind to local ip
	sockaddr_in localaddr = { 0 };
	localaddr.sin_family = AF_INET;
	localaddr.sin_port = 0;
	localaddr.sin_addr.s_addr = inet_addr(ip);

	if (WriteMemory(fpBind, &bSavedByteBind, sizeof(BYTE)) == FALSE) {
		MessageBox(NULL, L"Write Memory Error", L"DLL Injected",
			MB_OK);
		ExitThread(0);
	}

	BOOL b = bind(s, (sockaddr*)&localaddr, len);


	HookBind();
	return b;
}

int MyConnect(SOCKET s, sockaddr *name, int len) {
	
	// bind to local ip
	sockaddr_in localaddr = { 0 };
	localaddr.sin_family = AF_INET;
	//localaddr.sin_port = 0;
	localaddr.sin_addr.s_addr = inet_addr(ip);
	
	if (bind(s, (sockaddr*)&localaddr, sizeof(localaddr)) == SOCKET_ERROR) {
		/*int wError = WSAGetLastError();
		MessageBoxA(NULL, std::to_string(wError).c_str(), "DLL Injected",
			MB_OK);*/
	}

	/*MessageBoxA(NULL, "done", "DLL Injected",
		MB_OK);*/
		
	if (WriteMemory(fpConnect, &bSavedByte, sizeof(BYTE)) == FALSE) {
		MessageBox(NULL, L"Write Memory Error", L"DLL Injected",
			MB_OK);
		ExitThread(0);
	}

	BOOL b = connect(s, name, len);

	HookConnect();
	return b;

}

LONG WINAPI MyUnhandledExceptionFilter(LPEXCEPTION_POINTERS lpException) {
	if (lpException->ContextRecord->Rip == (DWORD_PTR)fpConnect)
		lpException->ContextRecord->Rip = (DWORD_PTR)MyConnect;
	if (lpException->ContextRecord->Rip == (DWORD_PTR)fpBind)
		lpException->ContextRecord->Rip = (DWORD_PTR)MyBind;

	return EXCEPTION_CONTINUE_EXECUTION;
}

BOOL WriteMemory(FARPROC fpFunc,const BYTE * b, SIZE_T size) {
	DWORD dwOldProt = 0;
	if (VirtualProtect(fpFunc, size, PAGE_EXECUTE_READWRITE, &dwOldProt) == FALSE)
		return FALSE;

	MoveMemory(fpFunc, b, size);

	return VirtualProtect(fpFunc, size, dwOldProt, &dwOldProt);
}

VOID HookConnect(VOID) {
	fpConnect = GetProcAddress(LoadLibrary(L"ws2_32"), "connect");
	if (fpConnect == NULL){
		MessageBox(NULL, L"No address :/", L"DLL Injected",
			MB_OK);
		return;
	}
	bSavedByte = *(LPBYTE)fpConnect;

	const BYTE bInt3 = 0xCC;

	if (WriteMemory(fpConnect, &bInt3, sizeof(BYTE)) == FALSE){
		MessageBox(NULL, L"Write Memory Error", L"DLL Injected",
			MB_OK);
		ExitThread(0);
	}
}

VOID HookBind(VOID) {
	fpBind = GetProcAddress(LoadLibrary(L"ws2_32"), "bind");
	if (fpBind == NULL) {
		MessageBox(NULL, L"No address :/", L"DLL Injected",
			MB_OK);
		return;
	}
	bSavedByteBind = *(LPBYTE)fpBind;

	const BYTE bInt3 = 0xCC;

	if(WriteMemory(fpBind, &bInt3, sizeof(BYTE)) == FALSE) {
		MessageBox(NULL, L"Write Memory Error", L"DLL Injected",
			MB_OK);
		ExitThread(0);
	}
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD trigger, LPVOID lpReserved)
{
	switch (trigger)
	{
	case DLL_PROCESS_ATTACH:
		// Make sure the namedpipe is created
		Sleep(2000);
		// get the ip to bind to using namedpipe
		getIp();

		if ((strlen(ip) != 0)&&(strlen(ip)<17)) {
			// Hook the connect function to bind to the right network adaptor
			SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)MyUnhandledExceptionFilter);
			HookBind();
			HookConnect();
		}
		else
		{
			MessageBox(NULL, L"Don't Have Ip", L"DLL Injected",
				MB_OK);
		}
		break;
	case DLL_THREAD_ATTACH:

		break;
	case DLL_THREAD_DETACH:
		break;
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}