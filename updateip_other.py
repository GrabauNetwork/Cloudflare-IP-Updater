import requests
#Update der IP-Adresse in Cloudflare
hostname = ""                                                                                           #Hostname des Records
cfzoneid = ""                                                               	                        #Cloudflare Zone-ID
cftoken = ""                                                                                            #CloudFlare User-Token
hostadress = ""
cfmainurl = "https://api.cloudflare.com/client/v4/zones/" + cfzoneid + "/dns_records"                   #CloudFlare API Main-URL
getip = "https://ipv6.icanhazip.com/"                                                                   #IP-Fetch-Server deklarieren (https://ipv6.icanhazip.com/ | https://ipv4.icanhazip.com/)

#Neue IP-Adresse erhalten
getnewip = requests.get(getip)                                                                          #Neue IP-Adresse Abfragen
newv6 = getnewip.text                                                                                   #Abfrage in Text umwandeln
newv6 = newv6.strip("\n") #Absatz aus Abfrage entfernen
newv6_split = newv6.split(':')
newv6 = ""
for i in range(0, 4):
    newv6 += newv6_split[i] + ":"
newv6 += hostadress

#Aktuellen Wert erhalten
req = requests.get(cfmainurl + "/?name=" + hostname,                                                    #Über den Hostname die aktuelle IP-Adresse aus Cloudflare abfragen
                   headers={"Authorization":"Bearer " + cftoken})                                       #Übergabe des Authorisations-Headers
gdata = req.json()                                                                                      #Abfrage in JSON umwandeln
for e in gdata["result"]:                                                                               #Json Result für Datenabfrage umwandeln
    oldv6 = e["content"]                                                                                #Alte IP-Adresse abfragen
    recordid = e["id"]                                                                                  #ID des Records abfragen
recordid = recordid.strip("\n")                                                                         #Absatz aus der Abfrage entfernen
rec = str(recordid)                                                                                     #ID des Records in String umwandeln
if(oldv6 == newv6):                                                                                     #Prüfen ob die alte IP mit der neu gezogenen IP übereinstimmt
    print("Deine aktuelle IP-Adresse (" + oldv6 + ") entspricht der Cloudflare-Adresse")                #Benutzerrückgabe
    print("Es ist also keine Aktion erforderlich!")                                                     #Benutzerrückgabe
    print("\nVorgang erfolgreich ausgeführt")                                                           #Benutzerrückgabe
else:                                                                                                   #Wenn sich die IP-Adresse geändert hat
    print("Deine IP-Adresse des Records " + hostname + " wird")                                         #Benutzerrückgabe welcher Record verändert wird 
    print("nun von " + oldv6 + " zu " + newv6 + " angepasst.")                                          #Benutzerrückgabe wie die IP geändert wird
    print("Dies kann einen Moment in Anspruch nehmen!")                                                 #Benutzerrückgabe
    setnewip = requests.put(cfmainurl + "/" + rec,                                                      #Angabe der Record-Adresse wo die Änderung geschehen soll
                            json={"type":e["type"],"name":e["name"],                                    #Übergabe der JSON Werte an die Cloudflare REST-API
                                  "ttl":e["ttl"], "proxied":e["proxied"],"content":newv6},              #Übergabe der JSON Werte an die Cloudflare REST-API
                            headers={'Authorization':'Bearer ' + cftoken})                              #Übergabe des Authorisations-Headers