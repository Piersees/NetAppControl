import speedtest


class SpeedTest:

    def __init__(self):

        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        s = speedtest.Speedtest() #objet speedtest

        s.get_servers(servers) #obtien tous les serveurs disponible

        s.get_best_server() #prend en fonction de l'emplacement le serveur le plus proche

        s.download() #Test le download, résultat en bit par second (a diviser par 10^6 pour avoir en Mb/s)

        s.upload() #Test le download, résultat en bit par second (a diviser par 10^6 pour avoir en Mb/s)

        s.results.share() #Créé un format png placer sur le serveur speedtest.net

        self.results_dict = s.results.dict() #met les différentes données dans un dictionnaire


    def returnResult(self):
        return self.results_dict
