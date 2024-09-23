# S-ADL_BAC_Detection Supplementary Codes

This repository is for supplementary codes used to explore and analyze the S-ADL Code and Dataset.

* Description of the paper and dataset: https://doi.org/10.1145/3613904.3642832
  * Hansoo Lee, Auk Kim, SangWon Bae, and Uichin Lee. 2024. S-ADL: Exploring Smartphone-based Activities of Daily Living to Detect Blood Alcohol Concentration in a Controlled Environment. In Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems (CHI '24). Association for Computing Machinery, New York, NY, USA, Article 1005, 1–25. https://doi.org/10.1145/3613904.3642832

Abstract: In public health and safety, precise detection of blood alcohol concentration (BAC) plays a critical role in implementing responsive interventions that can save lives. While previous research has primarily focused on computer-based or neuropsychological tests for BAC identification, the potential use of daily smartphone activities for BAC detection in real-life scenarios remains largely unexplored. Drawing inspiration from Instrumental Activities of Daily Living (I-ADL), our hypothesis suggests that Smartphone-based Activities of Daily Living (S-ADL) can serve as a viable method for identifying BAC. In our proof-of-concept study, we propose, design, and assess the feasibility of using S-ADLs to detect BAC in a scenario-based controlled laboratory experiment involving 40 young adults. In this study, we identify key S-ADL metrics, such as delayed texting in SMS, site searching, and finance management, that significantly contribute to BAC detection (with an AUC-ROC and accuracy of 81%). We further discuss potential real-life applications of the proposed BAC model.

Dataset URL: https://drive.google.com/drive/folders/0ACdSkIenytC8Uk9PVA 

## Citation
If you use this dataset in your research, please cite the following paper:
```
@inproceedings{lee2024s,
  title={S-ADL: Exploring Smartphone-based Activities of Daily Living to Detect Blood Alcohol Concentration in a Controlled Environment},
  author={Lee, Hansoo and Kim, Auk and Bae, SangWon and Lee, Uichin},
  booktitle={Proceedings of the CHI Conference on Human Factors in Computing Systems},
  year={2024},
  publisher={Association for Computing Machinery},
  address={New York, NY, USA},
  numpages={25},
  series = {CHI '24}
}
```

## Environment
We have run this code under the environment as below:
* OS: Ubuntu 20.04 installed with Windows Subsystem for Linux (WSL)
    * This code highly depends on a python multiprocessing library, [ray](https://www.ray.io/) which does not fully support Windows OS.
* CPU: AMD Ryzen 9 5900x 12-Core
    * This is not mandatory; you can run this code (with a minor modification) although you have the smaller number of cores.
* RAM: 128GB
    * This is not mandatory; we expected about 40GB of RAM to be required (but not tested).

In addition, you need to install [conda](https://conda.io/projects/conda/en/latest/index.html#) for managing packages and virtual environment.

## HOW-TO
---
