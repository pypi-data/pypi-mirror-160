# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold



class Evaluations:
    """ Evaluations class contains different evaluation methods 
    based on splitting the dataset per subject and/or per session.
    
    Args:
        dataset: Dataset from moabb.datasets
        
        paradigm: Paradigm from moabb.paradigms
        
        subjects: list of the ids of the subjects to be classified.
        
        clf: Pipeline of the steps to be followed.
    """
    
    
    def __init__(self, dataset, paradigm, subjects, clf):
        self.dataset = dataset
        self.paradigm = paradigm
        self.subjects = subjects
        self.clf = clf
        
        
    def CrossSubject(self):
        """  
        Evaluates the performance of the model trained on all subjects but one.
        
        Returns: 
            results: pd.DataFrame containing the accuracy score and the f1 
            scores for each class.
        
        """
        print("\nLoading data...")
        X, y, metadata = self.paradigm.get_data(dataset=self.dataset, subjects=self.subjects, return_epochs=1 )
        X = X.get_data()
        y = LabelEncoder().fit_transform(y)
        
        groups = metadata.subject.values
        cv = LeaveOneGroupOut()
            
        r = []
        for train, test in tqdm(cv.split(X, y, groups)):
            subject = groups[test[0]]
            y_pred = self.clf.fit(X[train], y[train]).predict(X[test])
            acc = accuracy_score(y[test], y_pred)
            report = classification_report(y[test], y_pred, output_dict =True, zero_division=0)
            f1_class0 = report['0']['f1-score']
            f1_class1 = report['1']['f1-score']
            f1_class2 = report['2']['f1-score']
            f1_class3 = report['3']['f1-score']
            r.append([int(subject), acc, f1_class0, f1_class1, f1_class2, f1_class3])
        results = pd.DataFrame(r, columns=['Subject', 'Accuracy', 'f1_class0', 'f1_class1','f1_class2','f1_class3'])
        return results
    
    
    
    def IntraSession(self):
        """  
        Evaluates the performance of the model trained on one session
        and tested on the same session of each subject separetely, 
        using 5 fold cv. 
        
        Returns: 
            results: pd.DataFrame containing the mean accuracy score 
            and the mean f1 scores for each class. 
        """
        
        r = []
        for i in tqdm(self.subjects):
            X, y, metadata = self.paradigm.get_data(dataset=self.dataset, subjects= [i], return_epochs=1)
            y = LabelEncoder().fit_transform(y)
            for session in np.unique(metadata.session):
                    ix = metadata.session == session
                    X_ = X[ix].get_data()
                    y_ = y[ix]
                    
                    cv =  StratifiedKFold(5, shuffle=True, random_state=42)
                    
                    accs = []; f1_0=[]; f1_1=[]; f1_2=[]; f1_3=[]
                    for train, test in cv.split(X_, y_):
                        self.clf.fit(X_[train], y_[train])
                        y_pred = self.clf.predict(X_[test])
                        acc = accuracy_score(y_[test], y_pred)
                        report = classification_report(y[test], y_pred, output_dict =True, zero_division=0)
                        f1_class0 = report['0']['f1-score']
                        f1_class1 = report['1']['f1-score']
                        f1_class2 = report['2']['f1-score']
                        f1_class3 = report['3']['f1-score']
                        accs.append(acc); f1_0.append(f1_class0); f1_1.append(f1_class1); 
                        f1_2.append(f1_class2); f1_3.append(f1_class3);
                    mean_acc = np.mean(np.array(accs)); mean_f1_0 = np.mean(np.array(f1_0)); mean_f1_1 = np.mean(np.array(f1_1));
                    mean_f1_2 = np.mean(np.array(f1_2)); mean_f1_3 = np.mean(np.array(f1_3))
                    r.append([i, session, mean_acc, mean_f1_0, mean_f1_1, mean_f1_2, mean_f1_3])
        results = pd.DataFrame(r, columns=['Subject','Session', 'Mean accuracy', 'Mean f1_class0', 'Mean f1_class1','Mean f1_class2','Mean f1_class3'])
        return results
    
    
    def IntraSubjectMixedSessions(self):
        """
        Evaluates the performance of the model for each subject  
        separetely, cancatenating the 2 sessions.
        
        Returns: 
            results: pd.DataFrame containing the mean accuracy score 
            and the mean f1 scores for each class.
        
        """
        
        r = []
        for i in tqdm(self.subjects):
            X, y, metadata = self.paradigm.get_data(dataset=self.dataset, subjects= [i], return_epochs=1)
            X = X.get_data()
            y = LabelEncoder().fit_transform(y)
    
            cv =  StratifiedKFold(5, shuffle=True, random_state=42)
            
            accs = []; f1_0=[]; f1_1=[]; f1_2=[]; f1_3=[]
            for train, test in cv.split(X, y):
                self.clf.fit(X[train], y[train])
                y_pred = self.clf.predict(X[test])
                acc = accuracy_score(y[test], y_pred)
                report = classification_report(y[test], y_pred, output_dict =True, zero_division=0)
                f1_class0 = report['0']['f1-score']
                f1_class1 = report['1']['f1-score']
                f1_class2 = report['2']['f1-score']
                f1_class3 = report['3']['f1-score']
                accs.append(acc); f1_0.append(f1_class0); f1_1.append(f1_class1); 
                f1_2.append(f1_class2); f1_3.append(f1_class3);
            mean_acc = np.mean(np.array(accs)); mean_f1_0 = np.mean(np.array(f1_0)); mean_f1_1 = np.mean(np.array(f1_1));
            mean_f1_2 = np.mean(np.array(f1_2)); mean_f1_3 = np.mean(np.array(f1_3))
            r.append([i, mean_acc, mean_f1_0, mean_f1_1, mean_f1_2, mean_f1_3])
        results = pd.DataFrame(r, columns=['Subject', 'Mean accuracy', 'Mean f1_class0', 'Mean f1_class1','Mean f1_class2','Mean f1_class3'])
        return results
    
    
    def IntraSubjectCrossSession(self):
        
        """
        Evaluates the performance of the model trained on only one 
        session and tested on the remaining on for each subject. 
        
        Returns: 
            results: pd.DataFrame containing the accuracy score 
            and the f1 scores for each class.
        
        """
        
        r = []
        for i in tqdm(self.subjects):
            X, y, metadata = self.paradigm.get_data(dataset=self.dataset, subjects= [i], return_epochs=1)
            X = X.get_data()
            y = LabelEncoder().fit_transform(y)
            groups = metadata.session.values
    
            cv = LeaveOneGroupOut()
                    
            for train, test in cv.split(X, y, groups):
                self.clf.fit(X[train], y[train])
                y_pred = self.clf.predict(X[test])
                session =  groups[test][0]
                acc = accuracy_score(y[test], y_pred)
                report = classification_report(y[test], y_pred, output_dict =True, zero_division=0)
                f1_class0 = report['0']['f1-score']
                f1_class1 = report['1']['f1-score']
                f1_class2 = report['2']['f1-score']
                f1_class3 = report['3']['f1-score']
                r.append([i, session, acc, f1_class0, f1_class1, f1_class2, f1_class3])
        results = pd.DataFrame(r, columns=['Subject','Session', 'Accuracy', 'f1_class0', 'f1_class1','f1_class2','f1_class3'])
        return results