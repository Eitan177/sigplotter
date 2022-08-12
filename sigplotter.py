import streamlit as st
import zipfile
import urllib.request
import glob
import SigProfilerMatrixGenerator
from SigProfilerMatrixGenerator import install as genInstall
import shutil
import os
from SigProfilerExtractor import sigpro as sig
import sys
import base64
import streamlit.components.v1 as components

curdir= os.getcwd()

def remove_old_vcf():
    vcfrem=glob.glob('input/*.vcf')
    for filepath in vcfrem:
        os.remove(filepath)
    vcfrem=glob.glob('input/input/*.vcf')    
    for filepath in vcfrem:
        os.remove(filepath)  

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1500" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)




if st.button('get reference genome'):
    st.write(os.path.dirname(SigProfilerMatrixGenerator.__file__))
    dirtest=os.path.dirname(SigProfilerMatrixGenerator.__file__)
    st.write(sys.path)
    urllib.request.urlretrieve('https://dl.dropboxusercontent.com/s/et97ewsct862x7m/references.zip?dl=0','references.zip')
    with zipfile.ZipFile('references.zip', 'r') as zip_ref:
        zip_ref.extractall('/home/appuser/venv/lib/python3.9/site-packages/SigProfilerMatrixGenerator')
    ##genInstall.install('GRCh37')

if not os.path.exists('input'):
    os.mkdir('input')

if not os.path.exists('input/input'):
    os.mkdir('input/input')

file_to_lookat=st.file_uploader('VCF upload here',type=[".vcf"],accept_multiple_files=True)
remove_old_vcf()

if file_to_lookat !=[]:
    bytes_data=file_to_lookat[0].read()
    with open(os.path.join("input",file_to_lookat[0].name),"wb") as f:
        f.write(bytes_data)
        f.close()
    
    #vcfuse=glob.glob('file_to_lookat[0].name')[0]
    #shutil.copy2(vcfuse,'input/'+vcfuse)
    #pdb.set_trace()
    with st.spinner('computing signatures'):
        sig.sigProfilerExtractor("vcf", "output", "input", minimum_signatures=1, maximum_signatures=3)
   
    show_pdf('output/SBS96/Suggested_Solution/COSMIC_SBS96_Decomposed_Solution/SBS96_Decomposition_Plots.pdf')
    
    components.iframe("https://cancer.sanger.ac.uk/signatures/sbs/", height=3000,width=800)
    show_pdf('output/ID83/Suggested_Solution/COSMIC_ID83_Decomposed_Solution/ID83_Decomposition_Plots.pdf')
    components.iframe("https://cancer.sanger.ac.uk/signatures/id/",height=3000,width=800)
    remove_old_vcf() 
