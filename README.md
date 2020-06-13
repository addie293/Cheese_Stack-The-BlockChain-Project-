# Subject Overview
This work consists of developing a crypto-currency system that has been inspired from bitcoin, but not being compatible with the latter. The system involves different kinds of elements, such as the a tracker, members, cheeses and a cheese stack. We have been able to successfully conduct transactions between different members and also mine new cheese. 
## Running the Project
The order of running the files are as follows:

   - Run tracker.py
   - Run proof\_of\_work.py<br>
   
Make sure the TCP addresses of the Tracker and the member are the same.
## Brief Architectural Description
**Tracker**: It is a server that contains the list of the members and their member IP address and port numbers. The tracker lets a new member know that there are availability of members in the network.<br><br>
**Member**: Members are miners looking to make transactions with each other. The member asks to be registered to the tracker by sending over it's socket address. It can also ask the tracker for a list of members so ask to make a transaction. In all, a member does the following:

- **Activates itself**: In this function, the member activates itself to start sniffing or dumping the cheese.
- **Reload Cheese**: Here, the member basically reloads a pre-existing cheese.
- **Sniffs Cheese**: The member sees if there are new cheese in the network.
- **Send Transaction Details**: In this function, the member creates anew cheese with a transaction and broadcasts the details of the transaction.
- **Share Transaction Details**: Broadcasts its own transaction details throughout the network.
- **Request Transaction Details**: One member can request the transaction detail of another.
<br><br> The last two functionalities work in cohesion with the proof\_of\_work.py module in the system

## Reference(s) used
- Swan, Melanie. Blockchain: Blueprint for a new economy. " O'Reilly Media, Inc.", 2015.
APA	
- Underwood, Sarah. "Blockchain beyond bitcoin." (2016): 15-17.
- Zheng, Zibin, et al. "Blockchain challenges and opportunities: A survey." International Journal of Web and Grid Services 14.4 (2018): 352-375.
- Eyal, Ittay, et al. "Bitcoin-ng: A scalable blockchain protocol." 13th {USENIX} symposium on networked systems design and implementation ({NSDI} 16). 2016.
- Drescher, Daniel. Blockchain basics. Vol. 276. Berkeley, CA: Apress, 2017.
- Qiu, Dongyu, and Rayadurgam Srikant. "Modeling and performance analysis of BitTorrent-like peer-to-peer networks." ACM SIGCOMM computer communication review 34.4 (2004): 367-378.
- Gupta, Minaxi, Paul Judge, and Mostafa Ammar. "A reputation system for peer-to-peer networks." Proceedings of the 13th international workshop on Network and operating systems support for digital audio and video. 2003.
- GitHub (link: https://github.com/dvf/blockchain)
- GitHub (link: https://github.com/UJM-INFO/2018-net-j)
- GitHub (link: https://github.com/lhartikk/naivechain)


