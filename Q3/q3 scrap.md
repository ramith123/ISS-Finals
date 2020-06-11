# Scrap file for ISS Question 3

## Things to look for
- [ ] VPN
- [ ] IPSec
- [ ] IDS
- [ ] DMZ 
- [ ] Authentication method
- [ ] Hashing a certain part (DOB and Last name etc.)
- [ ] A CDN
- [ ] A network layer protocol for remote and main

**N.B** : A CA certificate exists for the main server

## Actors
  1.  Database
  2.    Main Server
        -    Queries
  3.  Remote clients
  4.  Client router
        -   unsecured network between remote client and this router.
  5.  Server router
       - Unsecured network between main server and this router.

## Scenarios to consider
   1.   only release signed information (whatever this means.)
   2.   pre-compute digital signatures for performance reasons.
   3.   Constantly update remote sites. (Database is updated daily. **Appended is highlighted**)
   4.   Poor connection between remote and main.
   5.   Account for Insider attacks (info in [router](#Actors))
   6.   The client analyses the data
   7.   Internal network structure should be anonymous
        - DMZ
   8.   No possibility of a Dictionary attack
   9.   No possibility of eavesdropping between remote and server.

