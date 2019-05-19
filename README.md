# IBD-Network-Models-Reproduction (May 15-17, 2019)  

# Report
As part of the NLM Reproducibility Workshop, May 15-17, 2019, we tried to reproduce the study published in [Nature Genetics volume 49, pages 1437–1449 (2017)](https://www.nature.com/articles/ng.3947)

## Outline of the group's workflow
```
IBD-Repro_presentation.ipynb
```

## Reproducing figures

Supplementary Table 15/16 and reproduce Fig2

```
netweaver.Rmd
├── SupplTable15.csv
├── SupplTable16.csv
    ├──Fig2_repro.pdf
```

## Curating directory path

```
get_in_and_out.ipynb
├── example.csv
```

```
DirectoryNodes_EEM-wPaths.ipynb
├── DirectoryNodes.csv
├── NodeTypes_wPaths.csv
```
## Visualization
```
├── DirectoryNodes_wPaths.csv
├── NodeTypes_wPaths.csv
├── repotree.py
├── repotree.ipynb
├── PAPER_DATA-rt-ig.html
├── tree04.html
├── requirements.txt
```

#### Directories Tree via Fruchterman-Reingold Layout  
[tree04.html](http://htmlpreview.github.io/?https://github.com/NLM-Reproducibility-Project/IBD-Network-Models-Reproduction/master/tree04.html)
#### Directories Tree via Reingold-Tilford Layout
[PAPER_DATA-rt-ig.html](http://htmlpreview.github.io/?https://github.com/NLM-Reproducibility-Project/IBD-Network-Models-Reproduction/master/PAPER_DATA-rt-ig.html)
#### Code
```
├── repotree.py  - visualization for Reingold-Tilford Layout
├── repotree.ipynb
├── PAPER_DATA-rt-ig.html
├── tree04.html
├── requirements.txt - for repotree.py
```  
#### Visualization legend:  
red - code  
blue - data (ASCII)  
green - data (binary)   
black - directories  
magenta - everything else  

