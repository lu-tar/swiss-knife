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
2023/09/19 15:50:18.104114025 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:50:23.110789120 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:50:29.816542675 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:50:29.816666722 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:50:46.087863218 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:50:50.417482789 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:50:59.304294366 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:50:59.304421491 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:51:44.615639701 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 2, CO_CLIENT_DELETE_REASON_DEAUTH_OR_DISASSOC_REQ, Client state S_CO_RUN
2023/09/19 15:51:54.075202901 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:51:54.075342980 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:52:04.552921444 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:52:04.553027256 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:52:08.875774353 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_IP_LEARN_IN_PROGRESS
2023/09/19 15:55:08.583139538 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 2, CO_CLIENT_DELETE_REASON_DEAUTH_OR_DISASSOC_REQ, Client state S_CO_RUN
2023/09/19 15:55:32.785666872 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:55:32.785788474 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:55:34.705446845 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:55:43.321769704 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:56:05.568479853 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE, Client state S_CO_INIT
2023/09/19 15:56:05.568609326 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (ERR): MAC: 845f.04e7.d557  Failed to send client delete mobile. delete reason: 35, CO_CLIENT_DELETE_REASON_SAE_AUTH_FAILURE
2023/09/19 15:56:05.773374970 {wncd_x_R0-0}{1}: [dot11] [17435]: (ERR): MAC: 845f.04e7.d557  Dot11 update co assoc fail. Sent assoc failure to CO. delete reason: 54, CO_CLIENT_DELETE_REASON_DOT11_INVALID_PMKID
2023/09/19 15:56:05.773389224 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 54, CO_CLIENT_DELETE_REASON_DOT11_INVALID_PMKID, Client state S_CO_ASSOCIATING
2023/09/19 15:56:09.868174016 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
2023/09/19 15:56:14.879357285 {wncd_x_R0-0}{1}: [client-orch-sm] [17435]: (info): MAC: 845f.04e7.d557  Deleting the client, reason: 185, CO_CLIENT_DELETE_REASON_SAE_AUTH_IN_ASSOCIATED_STATE, Client state S_CO_RUN
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
Date: `2023/02/27`
Time: `14:41:15.703540`
Daemon: `{wncd_x_R0-0}{1}:`
Category: `[client-keymgmt]`
UnknownID: `[16602]:`
Severity: `(info):`
MAC: `MAC: c81c.fe19.f2e5`
Message: `EAP key M1 Sent successfully`

- Apro il file e lo divido per mac-address con una regex (esempio 2 mac-address)
- Di quei 2 file, uno per mac address, lo suddivido per associazioni e riassociazioni (non necessario su 9800)
- All'interno dei blocchi-associazione filtro i dati

Risultato prima versione

```python
[7, '2023/09/19', '15:49:46.963798763', '{wncd_x_R0-0}{1}:', '[auth-mgr] [17435]:', 'info', ' [845f.04e7.d557:capwap_900000a1] Session Start event called from SANET-SHIM, vlan: 0']
```