#Installation

After cloning the repository, run
    
      sudo python setup.py install

#Building/downloading definition graphs

Before you can use the module you'll need to get two precompiled definition graphs, [one](http://people.mokk.bme.hu/~recski/pymachine/4lang.pickle.gz) built from 4lang and [another](http://people.mokk.bme.hu/~recski/pymachine/longman.dep.pickle.gz) from LDOCE (you can also build your own graph from 4lang after downloading it from [GitHub](https://github.com/kornai/4lang))

Once you have the graph binaries, make sure your config file (machine.cfg or similar) points to them.

If you have any questions or comments or if you need technical help, please write to recski at mokk dot bme dot hu
