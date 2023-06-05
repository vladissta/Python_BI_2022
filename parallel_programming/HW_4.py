#!/usr/bin/env python
# coding: utf-8

# В формулировке заданий будет использоваться понятие **worker**. Это слово обозначает какую-то единицу параллельного выполнения, в случае питона это может быть **поток** или **процесс**, выбирайте то, что лучше будет подходить к конкретной задаче
# 
# В каждом задании нужно писать подробные аннотиции типов для:
# 1. Аргументов функций и классов
# 2. Возвращаемых значений
# 3. Классовых атрибутов (если такие есть)
# 
# В каждом задании нужно писать докстроки в определённом стиле (какой вам больше нравится) для всех функций, классов и методов

# # Задание 1 (7 баллов)

# В одном из заданий по ML от вас требовалось написать кастомную реализацию Random Forest. Её проблема состоит в том, что она работает медленно, так как использует всего один поток для работы. Добавление параллельного программирования в код позволит получить существенный прирост в скорости обучения и предсказаний.
# 
# В данном задании от вас требуется добавить возможность обучать случайный лес параллельно и использовать параллелизм для предсказаний. Для этого вам понадобится:
# 1. Добавить аргумент `n_jobs` в метод `fit`. `n_jobs` показывает количество worker'ов, используемых для распараллеливания
# 2. Добавить аргумент `n_jobs` в методы `predict` и `predict_proba`
# 3. Реализовать функционал по распараллеливанию в данных методах
# 
# В результате код `random_forest.fit(X, y, n_jobs=2)` и `random_forest.predict(X, y, n_jobs=2)` должен работать в ~1.5-2 раза быстрее, чем `random_forest.fit(X, y, n_jobs=1)` и `random_forest.predict(X, y, n_jobs=1)` соответственно
# 
# Если у вас по каким-то причинам нет кода случайного леса из ДЗ по ML, то вы можете написать его заново или попросить у однокурсника. *Детали* реализации ML части оцениваться не будут, НО, если вы поломаете логику работы алгоритма во время реализации параллелизма, то за это будут сниматься баллы
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, а также функции и классы из **sklearn** при помощи которых вы изначально писали лес

# In[1]:


from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

import numpy as np


# In[2]:


import threading
from concurrent.futures import ThreadPoolExecutor


# In[3]:


class RandomForestClassifierCustom(BaseEstimator):
    
    def __init__(self, n_estimators: int = 10, max_depth: int = None, 
                 max_features: int = None, random_state: int = 42) -> None:
        
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state

        self.trees = []
        self.feat_ids_by_tree = []

    def fit(self, X: np.ndarray, y: np.ndarray, n_jobs: int = 1) -> None:
        
        self.classes_ = sorted(np.unique(y))
        
        def one_thread_fit(self, X: np.ndarray, y: np.ndarray) -> None:
                
                np.random.seed(self.random_state)
                
                feats_rsm = np.random.choice(X.shape[1], 
                                             self.max_features,
                                             replace=False)

                self.feat_ids_by_tree.append(feats_rsm)

                boot_idx = np.random.choice(X.shape[0], 
                                            size=X.shape[0],
                                            replace=True)

                X_boot = X[boot_idx][:,feats_rsm]
                y_boot = y[boot_idx]

                dtc = DecisionTreeClassifier(max_depth=self.max_depth, 
                                       max_features=self.max_features,
                                       random_state=self.random_state)
                dtc.fit(X_boot, y_boot)
                self.trees.append(dtc)
        
        
        with ThreadPoolExecutor(n_jobs) as pool:
            
            pool.map(one_thread_fit,
                     [self] * (self.n_estimators + 1),
                     [X] * (self.n_estimators + 1), 
                     [y] * (self.n_estimators + 1))
            
        return self
        
        
    def predict_proba(self, X: np.ndarray, n_jobs: int = 1) -> np.ndarray[float]:
        
        probs = []
        
        def one_thread_predict_proba(self, X: np.ndarray, i: int) -> None:
            probs.append(self.trees[i].predict_proba(X[:,self.feat_ids_by_tree[i]]))
        
            
        with ThreadPoolExecutor(n_jobs) as pool:
            
            pool.map(one_thread_predict_proba,
                     [self] * (self.n_estimators + 1),
                     [X] * (self.n_estimators + 1), 
                     [i for i in range(self.n_estimators + 1)])
        
        return(np.mean(probs, axis=0))
    
    def predict(self, X: np.ndarray, n_jobs: int = 1) -> np.ndarray[int]:
        
        probas = self.predict_proba(X, n_jobs=n_jobs)
        predictions = np.argmax(probas, axis=1)
        return predictions
    

X, y = make_classification(n_samples=100000)


# In[4]:


random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)


# In[5]:


get_ipython().run_cell_magic('time', '', '\n_ = random_forest.fit(X, y, n_jobs=1)\n')


# In[6]:


get_ipython().run_cell_magic('time', '', '\npreds_1 = random_forest.predict(X, n_jobs=1)\n')


# In[7]:


random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)


# In[8]:


get_ipython().run_cell_magic('time', '', '\n_ = random_forest.fit(X, y, n_jobs=2)\n')


# In[9]:


get_ipython().run_cell_magic('time', '', '\npreds_2 = random_forest.predict(X, n_jobs=2)\n')


# In[10]:


(preds_1 == preds_2).all()# Количество worker'ов не должно влиять на предсказания


# #### Какие есть недостатки у вашей реализации параллельного Random Forest (если они есть)? Как это можно исправить? Опишите словами, можно без кода (+1 дополнительный балл)

# Ответ пишите тут

# # Задание 2 (9 баллов)

# Напишите декоратор `memory_limit`, который позволит ограничивать использование памяти декорируемой функцией.
# 
# Декоратор должен принимать следующие аргументы:
# 1. `soft_limit` - "мягкий" лимит использования памяти. При превышении функцией этого лимита должен будет отображён **warning**
# 2. `hard_limit` - "жёсткий" лимит использования памяти. При превышении функцией этого лимита должно будет брошено исключение, а функция должна немедленно завершить свою работу
# 3. `poll_interval` - интервал времени (в секундах) между проверками использования памяти
# 
# Требования:
# 1. Потребление функцией памяти должно отслеживаться **во время выполнения функции**, а не после её завершения
# 2. **warning** при превышении `soft_limit` должен отображаться один раз, даже если функция переходила через этот лимит несколько раз
# 3. Если задать `soft_limit` или `hard_limit` как `None`, то соответствующий лимит должен быть отключён
# 4. Лимиты должны передаваться и отображаться в формате `<number>X`, где `X` - символ, обозначающий порядок единицы измерения памяти ("B", "K", "M", "G", "T", ...)
# 5. В тексте warning'ов и исключений должен быть указан текщий объём используемой памяти и величина превышенного лимита
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, можно писать вспомогательные функции и/или классы
# 
# В коде ниже для вас предопределены некоторые полезные функции, вы можете ими пользоваться, а можете не пользоваться

# In[11]:


import os
import psutil
import time
import warnings
import sys
from typing import Callable


# In[12]:


symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
prefix = {}
for idx, s in enumerate(symbols):
    prefix[s] = 1 << (idx + 1) * 10


# In[13]:


def get_memory_usage() -> int:    # Показывает текущее потребление памяти процессом
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def bytes_to_human_readable(n_bytes: int) -> str:

    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n_bytes}B"


def byte_decode(size: str) -> int:
    num, pref = float(size[:-1]), size[-1]
    if pref == 'B':
        num_bytes = num 
    else:
        num_bytes = num  * prefix[pref]
    
    return num_bytes
        

def memory_limit(soft_limit: int = None, 
                 hard_limit: int = None,
                 poll_interval: int = 1) -> Callable:
    
    def decorator(func: Callable) -> Callable:
        
        def inner_function() -> None:
            
            thread_func = threading.Thread(target=func)
            thread_func.start()
            
            limit = soft_limit
            hard = False
            
            while True:
                mem_usage = get_memory_usage()
                if not thread_func.is_alive():
                    return
                if  mem_usage > byte_decode(limit):
                    if hard:
                        print(f'Memory limit is reached! Memory used: {bytes_to_human_readable(mem_usage)}')
                        return
                    else:
                        print(f'Warning! Memory used: {bytes_to_human_readable(mem_usage)}')
                        limit = hard_limit
                        hard = True
                        
                time.sleep(poll_interval)
                
        return inner_function
    return decorator


# In[14]:


@memory_limit(soft_limit="512M", hard_limit="1.5G", poll_interval=0.1)
def memory_increment() -> list[int]:
    """
    Функция для тестирования
    
    В течение нескольких секунд достигает использования памяти 1.89G
    Потребление памяти и скорость накопления можно варьировать, изменяя код
    """
    lst = []
    for i in range(50000000):
#         if i % 50000 == 0:
#             time.sleep(0.1)
        lst.append(i)
    return lst


# In[15]:


memory_increment()


# In[ ]:




