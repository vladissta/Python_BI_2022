# Genscan API

### About files:

- **requirements.txt** - files with requirement packages
```
pip install -r requirements.txt
```

- **genscan_module.py** - module itself  

Run in directory containing _genscan_module.py_ to import:
```
import genscan_module
from genscan_module import run_genscan
```

Usage example:
```
run_genscan(sequence=None, sequence_file='../data/sequence.fasta',
            organism="Vertebrate", exon_cutoff=1.00,
            sequence_name="Seq_1")
```
