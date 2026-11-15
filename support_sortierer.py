
import sqlite3

verbindung = sqlite3.connect('tickets.db')
cursor = verbindung.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL,
    kategorie TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

verbindung.commit()

# Supportanfragen

anfragen = []
anzahl = 0
cursor.execute('Select id, problem, kategorie, status FROM tickets')
for zeile in cursor.fetchall():
       anfrage = {
              'Ticket': zeile[0],
              'problem': zeile[1],
              'kategorie': zeile[2],
              'status': zeile[3]
       }
       anfragen.append(anfrage)


def ticket_anzeigen(anfrage):
         print(f"Ticket #{anfrage['Ticket']} | {anfrage['problem']} | Kategorie: {anfrage['kategorie']} | {anfrage['status']}")
def kategorie_bestimmen(suchtext):
    if 'anmeldung' in suchtext or 'passwort' in suchtext or 'login' in suchtext:
        return 'Benutzerkonto'
    elif 'tastatur' in suchtext or 'bildschirm' in suchtext or 'maus' in suchtext:
        return 'Hardware'
    elif 'internet' in suchtext or 'wlan' in suchtext or 'verbindung' in suchtext:
        return 'Netzwerk'
    else:
        return 'Sonstiges'

def ticket_erstellen(problem):
       suchtext = problem.lower()
       kategorie = kategorie_bestimmen(suchtext)

       cursor.execute('''
          INSERT INTO tickets (problem, kategorie, status)
          VALUES (?, ?, ?)
       ''', (problem, kategorie, "Offen"))

       verbindung.commit()

       ticketnummer = cursor.lastrowid

       anfrage = {
          'problem': problem,
          'kategorie': kategorie,
          'Ticket': ticketnummer,
          'status': 'Offen'
       }
                   
                
       anfragen.append(anfrage)
       print(f'Ticket #{ticketnummer} erstellt  | Kategorie: {kategorie}')

def tickets_auflisten():
    if not anfragen:
        print('Noch keine Tickets vorhanden.')
    else:
        for anfrage in anfragen:
            ticket_anzeigen(anfrage)

def offene_tickets_anzeigen():
      gefunden = False

      for anfrage in anfragen:
            if anfrage['status'] == 'Offen':
                  ticket_anzeigen(anfrage)
                  gefunden = True

      if not gefunden:
            print('Keine offenen Tickets vorhanden.')

def tickets_suchen():
      suchbegriff = input('Suchbegriff: ').strip().lower()

      if not suchbegriff:
                  print('Bitte gib einen Suchbegriff ein.')
                  return       
      
      gefunden = False
      
      for anfrage in anfragen:
            if suchbegriff in anfrage['problem'].lower():
                  ticket_anzeigen(anfrage)
                  gefunden = True
            
      if not gefunden:
                  print('Keine passenden Tickets gefunden.')
                  
def ticket_erledigen():
       ticketnummer = input('Welche Ticketnummer? ').strip()
       gefunden = False
       
       for anfrage in anfragen:
                     if str(anfrage['Ticket']) == ticketnummer:

                            if anfrage['status'] == 'Erledigt':
                                   print('Dieses Ticket ist bereits erledigt.')
                                   return
                            anfrage['status'] = 'Ereldigt'
                            anfrage['status'] = 'Erledigt'
                            cursor.execute('''
                            UPDATE tickets
                            SET status = ?
                            Where id = ?
                            ''', ('Erledigt', anfrage['Ticket']))
       
                            verbindung.commit()
                            print(f'Ticket #{anfrage['Ticket']} wurde als erledigt markiert.')
                            gefunden = True
                            break
       if not gefunden:
              print('Ticket nicht gefunden.')            

def ticket_loeschen():
       ticketnummer = input('Welche Ticketnummer möchtest du löschen? ').strip()
       gefunden = False
       
       for anfrage in anfragen:
              if str(anfrage['Ticket']) == ticketnummer:
                gefunden = True

                bestaetigung = input('Möchtest du dieses Ticket wirklich löschen? (ja/nein): ').strip().lower()

                if bestaetigung != 'ja':
                      print('Löschen abgebrochen')
                      return
                                    
                cursor.execute('''
                     DELETE FROM tickets
                     WHERE id = ?
                ''', (anfrage['Ticket'],))
       
                verbindung.commit()
       
                anfragen.remove(anfrage)
                print(f'Ticket #{ticketnummer} wurde gelöscht')
                break
       
       if not gefunden:
              print('Ticket nicht gefunden.')

def ticket_bearbeiten():
       ticketnummer = input('Welche Ticketnummer möchtest du bearbeiten? ').strip()
       gefunden = False

       for anfrage in anfragen:
              if str(anfrage['Ticket']) == ticketnummer:
                     gefunden = True
                     ticket_anzeigen(anfrage)
                     neues_problem = input('Neue Problembeschreibung: ').strip()

                     if not neues_problem:
                            print('Die Beschreibung darf nicht leer sein.')
                            break

                     neue_kategorie = kategorie_bestimmen(neues_problem.lower())
                     cursor.execute('''
                            UPDATE tickets
                            SET problem = ?, kategorie = ?
                            WHERE id = ?
                     ''', (neues_problem, neue_kategorie, anfrage['Ticket']))
                     
                     verbindung.commit()
                     
                     anfrage['problem'] = neues_problem
                     anfrage['kategorie'] = neue_kategorie
                     
                     print(f'Ticket #{ticketnummer} wurde aktualisiert.')
                     break

       if not gefunden:
              print('Ticket nicht gefunden.')

def statistik_anzeigen():
       cursor.execute('SELECT COUNT(*) FROM tickets')
       gesamt = cursor.fetchone()[0]
       
       cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "Offen"')
       offene_tickets = cursor.fetchone()[0]
       
       erledigte_tickets = gesamt - offene_tickets
       
       print('\n===== TICKET-STATISTIK =====')
       print(f'Tickets insgesamt: {gesamt}')
       print(f'Offene Tickets: {offene_tickets}')
       print(f'Erledigte Tickets: {erledigte_tickets}')
       print('===========================')
       
                      
       
       cursor.execute('''
       SELECT kategorie, COUNT(*)
       FROM tickets
       GROUP BY kategorie
       ''')
       
       kategorien = cursor.fetchall()
       
       print('\nTickets nach Kategorien:')
       
       for kategorie, anzahl in kategorien:
              print(f'{kategorie}: {anzahl}')
       
       print('==============================')
       
def hilfe_anzeigen():
    print('\n===== IT-TICKET-SYSTEM =====')
    print('Verfügbare Befehle:')
    print('liste       - Alle Tickets anzeigen')
    print('offen       - Offene Tickets anzeigen')
    print('suchen      - Tickets durchsuchen')
    print('erledigen   - Ticket abschließen')
    print('bearbeiten  - Ticket bearbeiten')
    print('löschen     - Ticket löschen')
    print('statistik   - Ticketstatistik anzeigen')
    print('hilfe       - Befehlsübersicht anzeigen')
    print('ende        - Programm beenden')
    print('============================')
    print('Zum Erstellen eines Tickets einfach das Problem eingeben.\n')       

hilfe_anzeigen()

while True:

        problem = input('Beschreibe dein IT-Problem: ').strip()
        suchtext = problem.lower()
        
        
        if suchtext == 'ende':
                print(f'Du hast insgesamt {len(anfragen)} Tickets gespeichert.')
                print('Erstellte Anfragen:')
                for anfrage in anfragen:
                       ticket_anzeigen(anfrage)
                print('Bis bald.')
                break
        
        elif suchtext == 'offen':
              offene_tickets_anzeigen()
                
        elif suchtext == 'suchen':
              tickets_suchen()                    
                
        elif suchtext == 'liste':
               tickets_auflisten()
                
        elif suchtext == 'erledigen':
               ticket_erledigen()
                
        elif suchtext == 'löschen':
               ticket_loeschen()
                    

        elif suchtext == 'bearbeiten':
               ticket_bearbeiten()    
        
        elif suchtext == 'statistik':
               statistik_anzeigen()

        elif suchtext == 'hilfe':
              hilfe_anzeigen()
               
        else:
            if not problem:
                   print('Bitte beschreibe dein IT-Problem.')
                   continue

            ticket_erstellen(problem)

verbindung.close()        
        
                 
        
                