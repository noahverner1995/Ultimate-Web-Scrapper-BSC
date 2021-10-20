<h1>Introducing: Block Scrapper BSC</h1>

A very sophisticated and robust program built on Python that is capable of seek, find and save from a set of the most recent validated blocks in bscscan.com, those transactions that match 2 specific parameters (which are "_PancakeSwap: Router v2_" as _**destiny**_ and a **_BNB Value_** greater than **2.15** and less than **16.2**), for then filtrering them using a dictionary and 3 extra parameters (which are "_Hodlers_" greater than **3000** and less than **20000**, "_Transactions_" greater than **2 times** the number of _Hodlers_, and a _contract age_ younger than **26 (days)**) in a single DataFrame.

This program also prints at the end of its process, the time (format HH:MM:SS.MS) it took to analyze a specific array of blocks, save the desired data and export it as a single DataFrame.

Also, a few csv files are left as sample.

It is expected that this program becomes a very useful application in future developments related to investments within decentralized exchanges in public blockchains.

Thanks to **@felipesalda** for his contribution in building this solution.
