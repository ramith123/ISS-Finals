# Scrap file for ISS Question 3


## Actors
  1.  Database

  2.    Main Server
        -    Queries
  3.  Remote clients
  4.  Client router
        -   unsecured network between remote client and this router.
  5.  Server router
       - Unsecured network between main server and this router.
  6.  Firewalls and dmz between over the offices


## Scenarios to consider
   1.   only release signed information (whatever this means.)
   1.   pre-compute digital signatures for performance reasons.
        - Compute hash values for dob+name. compute HMAC when sending data, using symmetric keys (AES) between client and server. (That way you can have different Symmetric keys per connection.)
   2.   Constantly update remote sites. (Database is updated daily. **Appended is highlighted**)
           - Sql restrictions. (Do not accept DELETE. INSERT and SELECT )
   3.   Poor connection between remote and main.
        -  Compression
        -  ATM protocol instead of IP
   
   4.   Account for Insider attacks (info in [router](#Actors))
         - Disk level encryption,
   5.   The client analyses the data
        -  generate HMAC using message and shared key.
   6.   Internal network structure should be anonymous
        - DMZ and vpn
   7.   No possibility of a Dictionary attack.
        - salt, IDS
   8.   No possibility of eavesdropping between remote and server.
        -  IPSEC through VPN (User authentication is integrated compare to SSL)
   9.   Check for XSS and SQL Injections
         -   Escape Queries

## Things to look for
- [ ] VPN
- [ ] IPSec
- [ ] IDS
- [ ] DMZ 
- [ ] Authentication method
- [ ] Hashing a certain part (DOB and Last name etc.)
- [ ] A CDN
- [ ] A network layer protocol for remote and main
- [ ] salt
- [ ] Escape Queries
- [ ] Disk level encryption, store raw info on a different database

**N.B** : A CA certificate exists for the main server
