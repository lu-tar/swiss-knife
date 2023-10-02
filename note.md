# Building a custom parser

# Dedug file 9800

Association received
```
2023/09/19 15:49:46.962897741 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (note): MAC: 845f.04e7.d557  Association received. BSSID 1484.7340.a8cd, WLAN MOBILE, Slot 1 AP 1484.7340.a8c0, mon-0b-ap-164
```
Association and re-association success
```
2023/09/19 15:49:46.963505395 {wncd_x_R0-0}{1}: [dot11] [17435]: (note): MAC: 845f.04e7.d557  Association success. AID 6, Roaming = False, WGB = False, 11r = False, 11w = True Fast roam = False

2023/09/19 15:57:23.471484913 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (note): MAC: 845f.04e7.d557  Re-Association received. BSSID 1484.7340.ec6d, WLAN MOBILE, Slot 1 AP 1484.7340.ec60, mon-1b-ap-172, old BSSID 1484.7340.a8cd
```
client-keymgmt success and failure
```
2023/09/19 15:49:46.971657310 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  EAP key M1 Sent successfully
2023/09/19 15:49:46.971665274 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  Client key-mgmt state transition: S_INITPMK -> S_PTK_START
2023/09/19 15:49:46.971710520 {mobilityd_R0-0}{1}: [mm-dgram-io] [17992]: (debug): MAC: 0000.0000.0000 Sending message: pmk_update to group: default
2023/09/19 15:49:46.982424869 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557   M2 Status: EAP key M2 validation success
2023/09/19 15:49:46.982535519 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  EAP key M3 Sent successfully
2023/09/19 15:49:46.982536773 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  Client key-mgmt state transition: S_PTK_START -> S_PTKINITNEGOTIATING
2023/09/19 15:49:46.986368190 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  M4 Status: EAP key M4 validation is successful
2023/09/19 15:49:46.986370726 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (note): MAC: 845f.04e7.d557  EAP Key management successful. AKM:SAE Cipher:CCMP WPA Version: WPA3
2023/09/19 15:49:46.986392260 {wncd_x_R0-0}{1}: [client-keymgmt] [17435]: (info): MAC: 845f.04e7.d557  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_PTKINITDONE

2023/02/27 14:42:03.151081 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  EAP key M1 Sent successfully
2023/02/27 14:42:03.151085 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTKINITDONE -> S_PTK_START
2023/02/27 14:42:03.171795 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5   M2 Status: EAP key M2 validation success
2023/02/27 14:42:03.171889 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  EAP key M3 Sent successfully
2023/02/27 14:42:03.171891 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTK_START -> S_PTKINITNEGOTIATING
2023/02/27 14:42:04.171522 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Keymgmt: resend eapol key m3. Retrasmitting EAP key packet M3
2023/02/27 14:42:04.171619 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_PTKINITNEGOTIATING
2023/02/27 14:42:04.324664 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (ERR): MAC: c81c.fe19.f2e5  Keymgmt: Failed to validate eapol key m4. Received wrong replay counter. stop processing
2023/02/27 14:42:04.324669 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_PTKINITNEGOTIATING
2023/02/27 14:42:05.171758 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Keymgmt: resend eapol key m3. Retrasmitting EAP key packet M3
2023/02/27 14:42:05.171863 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_PTKINITNEGOTIATING
2023/02/27 14:42:06.171706 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (ERR): MAC: c81c.fe19.f2e5  Keymgmt: Failed to eapol key m3 retransmit failure. Max retries for M3 over
2023/02/27 14:42:06.171720 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Keymgmt: eapol key failure. Sending client key exchange failure to auth fsm,reason code: 89
2023/02/27 14:42:06.171736 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_KEYMGMT_CLIENT_DELETE
```
client-iplearn
```
2023/09/19 15:49:47.171126851 {wncd_x_R0-0}{1}: [client-iplearn] [17435]: (note): MAC: 845f.04e7.d557  Client IP learn successful. Method: DHCP IP: 10.0.0.145
```
```
2023/09/19 15:49:47.171926572 {wncd_x_R0-0}{1}: [errmsg] [17435]: (debug): %CLIENT_ORCH_LOG-7-CLIENT_MOVED_TO_RUN_STATE: R0/0: wncd: Username (null), MAC: 845f.04e7.d557, IP 10.0.0.145 associated to AP (mon-0b-ap-164) with SSID (MOBILE)
```

deleting
```
2023/09/19 15:49:48.711160702 {wncd_x_R0-0}{1}: [dot11] [17435]: (info): MAC: 845f.04e7.d557  Dot11 receive SAE AUTH COMMIT message in ASSOCIATED State
2023/09/19 15:49:48.711189058 {wncd_x_R0-0}{1}: [dot11] [17435]: (info): MAC: 845f.04e7.d557  Parsing SAE COMMIT Message- Successful
2023/09/19 15:49:48.711204010 {wncd_x_R0-0}{1}: [dot11] [17435]: (info): MAC: 845f.04e7.d557  Dot11 process SAE Commit message post successfully parsing it
2023/09/19 15:49:48.711204866 {wncd_x_R0-0}{1}: [dot11] [17435]: (info): MAC: 845f.04e7.d557  Dot11 process SAE AUTH COMMIT in ASSOCIATED State, triggering client cleanup
2023/09/19 15:49:48.711356829 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:49:48.711460112 {wncd_x_R0-0}{1}: [errmsg] [17435]: (debug): %CLIENT_ORCH_LOG-7-CLIENT_MOVED_TO_DELETE_STATE: R0/0: wncd: Username (null), MAC: 845f.04e7.d557, IP fe80::10ed:705a:9dba:dc43 10.0.0.145 disconnected from AP (mon-0b-ap-164) with SSID (MOBILE)
2023/09/19 15:49:48.711460790 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (note): MAC: 845f.04e7.d557  Client delete initiated. Reason: CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, details: , fsm-state transition 00|00|00|00|00|00|00|00|00|00|00|00|00|00|00|00|01|07|15|1a|1b|2c|37|46|48|4a|4c|51|60|62|83|aa|
2023/09/19 15:49:48.711606615 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (note): MAC: 845f.04e7.d557  Delete mobile payload sent for BSSID: 1484.7340.a8cd WTP mac: 1484.7340.a8c0 slot id: 1 
2023/09/19 15:49:48.711617959 {wncd_x_R0-0}{1}: [client-orch-state] [17435]: (note): MAC: 845f.04e7.d557  Client state transition: S_CO_RUN -> S_CO_DELETE_IN_PROGRESS
```

reasons
```
$ cat 'debugTrace_845f.04e7.d557(2).txt' | grep 'reason'
2023/09/19 15:46:08.412807892 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 2, CO_CLIENT_DELETE_REASON_DEAUTH_OR_DISASSOC_REQ, Client state S_CO_RUN
2023/09/19 15:49:46.127867824 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:49:46.128009461 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:49:48.711356829 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:49:52.301440045 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:49:59.010607990 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:49:59.010749423 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
```

## Pseudocodice
- Devo rendere il file cronologico splittandolo come un csv (Pandas?)

```
2023/02/27 14:41:15.703540 {wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  EAP key M1 Sent successfully
```

Diventa

```csv
2023/02/27,14:41:15.703540,{wncd_x_R0-0}{1}: [client-keymgmt] [16602]: (info): MAC: c81c.fe19.f2e5  EAP key M1 Sent successfully
```
- Date: `2023/02/27`
- Time: `14:41:15.703540`
- Daemon: `{wncd_x_R0-0}{1}:`
- Category: `[client-keymgmt]`
- UnknownID: `[16602]:`
- Severity: `(info):`
- MAC: `MAC: c81c.fe19.f2e5`
- Message: `EAP key M1 Sent successfully`

- Apro il file e lo divido per mac-address con una regex (esempio 2 mac-address)
- Di quei 2 file, uno per mac address, lo suddivido per associazioni e riassociazioni (non necessario su 9800)
- All'interno dei blocchi-associazione filtro i dati

Risultato prima versione

```python
[7, '2023/09/19', '15:49:46.963798763', '{wncd_x_R0-0}{1}:', '[auth-mgr] [17435]:', 'info', ' [845f.04e7.d557:capwap_900000a1] Session Start event called from SANET-SHIM, vlan: 0']
```

## Parsing

Rimosso `Logging display requested on 2023/09/19 16:13:58 (ITALIA) for Hostname: [mon-a2-wlc-01], Model: [C9800-L-F-K9        ], Version: [17.09.03], SN: [FOC26290JZ8], MD_SN: [FCL262900CK]` da in cima al file, valutare se farci qualcosa.

Fondamentale filtrare per `[client-orch-state]` per avere uno storico degli eventi.

## How to use variables in SQL statement in Python?
```python
# Multiple values single statement/execution
c.execute('SELECT * FROM stocks WHERE symbol=? OR symbol=?', ('RHAT', 'MSO'))
print c.fetchall()
c.execute('SELECT * FROM stocks WHERE symbol IN (?, ?)', ('RHAT', 'MSO'))
print c.fetchall()
# This also works, though ones above are better as a habit as it's inline with syntax of executemany().. but your choice.
c.execute('SELECT * FROM stocks WHERE symbol=? OR symbol=?', 'RHAT', 'MSO')
print c.fetchall()
# Insert a single item
c.execute('INSERT INTO stocks VALUES (?,?,?,?,?)', ('2006-03-28', 'BUY', 'IBM', 1000, 45.00))
```

## basic_complete
```python
import cmd2

class MyCmd(cmd2.Cmd):
    def __init__(self):
        super().__init__()

    def do_hello(self, args):
        """Print a greeting."""
        print("Hello, " + args)

    def do_greet(self, args):
        """Greet someone."""
        print("Greeted: " + args)

    def basic_complete(self, text, line, begidx, endidx):
        """Custom tab completion for the 'hello' and 'greet' commands."""
        if line.strip().startswith("hello"):
            completions = ['world', 'there', 'cmd2']
        elif line.strip().startswith("greet"):
            completions = ['John', 'Alice', 'Bob']
        else:
            completions = []

        return [comp for comp in completions if comp.startswith(text)]

if __name__ == '__main__':
    app = MyCmd()
    app.cmdloop()
```
In this updated script, we've added a new command do_greet that takes a single argument and prints a greeting. We've also extended the basic_complete function to provide tab completion for both the do_hello and do_greet commands. The logic for completions is based on the prefix of the entered command (hello or greet).
Now, when you run the script and use the do_greet command, you'll get tab completion suggestions based on the input.