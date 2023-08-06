# -*- coding: utf-8 -*-
from . import Evaluations as ev

from pyriemann.estimation import Covariances
from pyriemann.tangentspace import TangentSpace
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA



def run(dataset, paradigm, subjects):
    """
    Main function, transforms the data using Tangent Space decoding and 
    PCA and classifies the components using SVC classifier. Next, it 
    evaluates the model based on the evaluation technique that the subject \
    has chosen and displays the results.
    """
    
    evaluation = str(input("Select evaluation method of the model (CrossSubject/IntraSession/IntraSubjectMixedSessions/IntraSubjectCrossSession) "))
    
    clf = Pipeline([
                ('cov' ,Covariances("oas")) ,
                ('tangent', TangentSpace(metric="riemann")),
                ('PCA', PCA(n_components=0.95)),
                ('SVC', OneVsRestClassifier(SVC(kernel="linear"))) ])
            
    if evaluation == "CrossSubject":
        results = ev(dataset, paradigm, subjects, clf).CrossSubject()
        
    elif evaluation == "IntraSession":
        results = ev(dataset, paradigm, subjects, clf).IntraSession()
        
    elif evaluation == "IntraSubjectMixedSessions":
        results = ev(dataset, paradigm, subjects, clf).IntraSubjectMixedSessions()
        
    elif evaluation == "IntraSubjectCrossSession":
        results = ev(dataset, paradigm, subjects, clf).IntraSubjectCrossSession()
        
    else:
        raise ValueError(f"Method: {evaluation} not found. Select an option from the parenthesis.")
        
    print(results)


