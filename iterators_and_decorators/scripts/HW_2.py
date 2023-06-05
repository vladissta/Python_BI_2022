#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (2 балла)

# Напишите класс `MyDict`, который будет полностью повторять поведение обычного словаря, за исключением того, что при итерации мы должны получать и ключи, и значения.
# 
# **Модули использовать нельзя**

# In[1]:


class MyDict(dict):

    def __iter__(self):
        for key, value in self.items():
            yield key, value


# In[2]:


dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})
for key, value in dct:
    print(key, value)   


# In[3]:


for key, value in dct.items():
    print(key, value)


# In[4]:


for key in dct.keys():
    print(key)


# In[5]:


dct["c"] + dct["d"]


# # Задание 2 (2 балла)

# Напишите функцию `iter_append`, которая "добавляет" новый элемент в конец итератора, возвращая итератор, который включает изначальные элементы и новый элемент. Итерироваться по итератору внутри функции нельзя, то есть вот такая штука не принимается
# ```python
# def iter_append(iterator, item):
#     lst = list(iterator) + [item]
#     return iter(lst)
# ```
# 
# **Модули использовать нельзя**

# In[6]:


def iter_append(iterator, item):

    yield from iterator
    yield from iter([item])


# In[7]:


my_iterator = iter([1, 2, 3])


# In[8]:


new_iterator = iter_append(my_iterator, 4)


# In[9]:


for element in new_iterator:
    print(element)


# In[10]:


for element in new_iterator:
    print(element)


# # Задание 3 (5 баллов)

# Представим, что мы установили себе некотурую библиотеку, которая содержит в себе два класса `MyString` и `MySet`, которые являются наследниками `str` и `set`, но также несут и дополнительные методы.
# 
# Проблема заключается в том, что библиотеку писали не очень аккуратные люди, поэтому получилось так, что некоторые методы возвращают не тот тип данных, который мы ожидаем. Например, `MyString().reverse()` возвращает объект класса `str`, хотя логичнее было бы ожидать объект класса `MyString`.
# 
# Найдите и реализуйте удобный способ сделать так, чтобы подобные методы возвращали экземпляр текущего класса, а не родительского. При этом **код методов изменять нельзя**
# 
# **+3 дополнительных балла** за реализацию того, чтобы **унаследованные от `str` и `set` методы** также возвращали объект интересующего нас класса (то есть `MyString.replace(..., ...)` должен возвращать `MyString`). **Переопределять методы нельзя**
# 
# **Модули использовать нельзя**

# In[11]:


# Ваш код где угодно, но не внутри методов


class MyString(str):       

    def proper_class_wrapper(func):
        def inner_fun(self):
            res = func(self)
            return type(self)(res)
        return inner_fun

    @proper_class_wrapper
    def reverse(self):
        return self[::-1]
    
    @proper_class_wrapper
    def make_uppercase(self):
        return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])
    
    @proper_class_wrapper
    def make_lowercase(self):
        return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])
    
    @proper_class_wrapper
    def capitalize_words(self):
        return " ".join([word.capitalize() for word in self.split()])
    
    
class MySet(set):

    def proper_class_wrapper(func):
        def inner_fun(self, other):
            res = func(self, other)
            return type(self)(res)
        return inner_fun
    
    def is_empty(self):
        return len(self) == 0
    
    def has_duplicates(self):
        return len(self) != len(set(self))
    
    @proper_class_wrapper
    def union_with(self, other):
        return self.union(other)
    
    @proper_class_wrapper
    def intersection_with(self, other):
        return self.intersection(other)
    
    @proper_class_wrapper
    def difference_with(self, other):
        return self.difference(other)


# In[12]:


string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})

print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))


# # Задание 4 (5 баллов)

# Напишите декоратор `switch_privacy`:
# 1. Делает все публичные **методы** класса приватными
# 2. Делает все приватные методы класса публичными
# 3. Dunder методы и защищённые методы остаются без изменений
# 4. Должен работать тестовый код ниже, в теле класса писать код нельзя
# 
# **Модули использовать нельзя**

# In[13]:


def switch_privacy(orig_class):

    attrs = []

    for attr in dir(orig_class):
        if not attr[-2:] == '__':
            attrs.append(attr)

    for attr in attrs:

        if orig_class.__name__ in attr:
            setattr(orig_class, attr.split('__')[1], getattr(orig_class, attr))
            delattr(orig_class, attr)

        elif attr[0] != '_':
            setattr(orig_class, f'_{orig_class.__name__}__{attr}', getattr(orig_class, attr))
            delattr(orig_class, attr)

    return orig_class


# In[14]:


@switch_privacy
class ExampleClass:
    # Но не здесь
    def public_method(self):
        return 1
    
    def _protected_method(self):
        return 2
    
    def __private_method(self):
        return 3
    
    def __dunder_method__(self):
        pass


# In[15]:


test_object = ExampleClass()

test_object._ExampleClass__public_method()   # Публичный метод стал приватным


# In[16]:


test_object.private_method()   # Приватный метод стал публичным


# In[17]:


test_object._protected_method()   # Защищённый метод остался защищённым


# In[18]:


test_object.__dunder_method__()   # Дандер метод не изменился


# In[19]:


hasattr(test_object, "public_method"), hasattr(test_object, "private")   # Изначальные варианты изменённых методов не сохраняются


# # Задание 5 (7 баллов)

# Напишите [контекстный менеджер](https://docs.python.org/3/library/stdtypes.html#context-manager-types) `OpenFasta`
# 
# Контекстные менеджеры это специальные объекты, которые могут работать с конструкцией `with ... as ...:`. В них нет ничего сложного, для их реализации как обычно нужно только определить только пару dunder методов. Изучите этот вопрос самостоятельно
# 
# 1. Объект должен работать как обычные файлы в питоне (наследоваться не надо, здесь лучше будет использовать **композицию**), но:
#     + При итерации по объекту мы должны будем получать не строку из файла, а специальный объект `FastaRecord`. Он будет хранить в себе информацию о последовательности. Важно, **не строки, а именно последовательности**, в fasta файлах последовательность часто разбивают на много строк
#     + Нужно написать методы `read_record` и `read_records`, которые по смыслу соответствуют `readline()` и `readlines()` в обычных файлах, но они должны выдавать не строки, а объект(ы) `FastaRecord`
# 2. Конструктор должен принимать один аргумент - **путь к файлу**
# 3. Класс должен эффективно распоряжаться памятью, с расчётом на работу с очень большими файлами
#     
# Объект `FastaRecord`. Это должен быть **датакласс** (см. про примеры декораторов в соответствующей лекции) с тремя полями:
# + `seq` - последовательность
# + `id_` - ID последовательности (это то, что в фаста файле в строке, которая начинается с `>` до первого пробела. Например, >**GTD326487.1** Species anonymous 24 chromosome) 
# + `description` - то, что осталось после ID (Например, >GTD326487.1 **Species anonymous 24 chromosome**)
# 
# 
# Напишите демонстрацию работы кода с использованием всех написанных методов, обязательно добавьте файл с тестовыми данными в репозиторий (не обязательно большой)
# 
# **Можно использовать модули из стандартной библиотеки**

# In[20]:


import os
import re
from dataclasses import dataclass


# In[21]:


@dataclass
class FastaRecord:
    id_: str
    description: str
    seq: str
    

class OpenFasta:
    
    __current_line = None

    def __init__(self, path): # here only path!
        self.path = path
        self.file_obj = None
        self.text = None
    
    def __enter__(self):
        self.file_obj = open(self.path)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
            self.file_obj.close()
    
    def __iter__(self):
        while True:
            try:
                yield self.read_record()
            except StopIteration:
                break
    
                  
    def read_record(self):
        
        if not self.__current_line:
            for line in self.file_obj:
                if line.strip() == "":
                    continue
                elif re.match('>', line):
                    self.__current_line = line
                    break
                    
        if self.__current_line:
            space = self.__current_line.find(' ')
            id_ = self.__current_line[1:space].strip()
            seq = []
            description = self.__current_line[space+1:].strip()

        for line in self.file_obj:
            if line.strip() == "":
                continue
            elif re.match('>', line):
                self.__current_line = line
                return FastaRecord(id_, description, ''.join(seq))
            else:
                seq.append(line.strip())
        else:
            if not seq:
                raise StopIteration('There are no more fasta records')
            return FastaRecord(id_, description, ''.join(seq))

    
    def read_records(self):
        records = []
        for line in self.file_obj:
            records.append(self.read_record())
        return records


# In[23]:


with OpenFasta('../data/seq.fasta') as fasta:
    
    for record in fasta:
        print(f"id of the first record: {record.id_}")
        print()
        break
    
    print(f"FastaRecord object:\n{fasta.read_record()}")
    print()
    fasta.read_record()
    fasta.read_record()
    fasta.read_record()
    fasta.read_record()
    fasta.read_record()
    
    print(f'Last FastaRecord object:\n{fasta.read_records()}')
    


# # Задание 6 (7 баллов)

# 1. Напишите код, который позволит получать все возможные (неуникальные) генотипы при скрещивании двух организмов. Это может быть функция или класс, что вам кажется более удобным.
# 
# Например, все возможные исходы скрещивания "Aabb" и "Aabb" (неуникальные) это
# 
# ```
# AAbb
# AAbb
# AAbb
# AAbb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# aabb
# aabb
# aabb
# aabb
# ```
# 
# 2. Напишите функцию, которая вычисляет вероятность появления определённого генотипа (его ожидаемую долю в потомстве).
# Например,
# 
# ```python
# get_offspting_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Аabb")   # 0.5
# 
# ```
# 
# 3. Напишите код, который выводит все уникальные генотипы при скрещивании `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` и `'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН'`, которые содержат в себе следующую комбинацию аллелей `'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл'`
# 4. Напишите код, который расчитывает вероятность появления генотипа `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` при скрещивании `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн` и `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн`
# 
# Важные замечания:
# 1. Порядок следования аллелей в случае гетерозигот всегда должен быть следующим: сначала большая буква, затем маленькая (вариант `AaBb` допустим, но `aAbB` быть не должно)
# 2. Подзадачи 3 и 4 могут потребовать много вычислительного времени (до 15+ минут в зависимости от железа), поэтому убедитесь, что вы хорошо протестировали написанный вами код на малых данных перед выполнением этих задач. Если ваш код работает **дольше 20 мин**, то скорее всего ваше решение не оптимально, попытайтесь что-нибудь оптимизировать. Если оптимальное решение совсем не получается, то попробуйте из входных данных во всех заданиях убрать последний ген (это должно уменьшить время выполнения примерно в 4 раза), но **за такое решение будет снято 2 балла**
# 3. Несмотря на то, что подзадания 2, 3 и 4 возможно решить математически, не прибегая к непосредственному получению всех возможных генотипов, от вас требуется именно brute-force вариант алгоритма
# 
# **Можно использовать модули из стандартной библиотеки питона**, но **за выполнение задания без использования модулей придусмотрено +3 дополнительных балла**

# ### 1.

# In[24]:


import itertools


# In[25]:


def all_genotypes(parent1="Aabb", parent2="Aabb"):
    
    all_genotypes = []
    for i in range(0, len(parent1), 2):
        genotype = []
        for el in itertools.product(parent1[i:i+2], parent2[i:i+2]):
            genotype.append(sorted(list(el)))
        all_genotypes.append(genotype)
    
    for combination in itertools.product(*all_genotypes):
            patially_joined = map(lambda x: ''.join(x), combination)
            print(''.join(patially_joined))


# In[26]:


all_genotypes()


# ### 2. maybe too much mathematics

# In[27]:


def probability_genotype(parent1="Aabb", parent2="Aabb", 
                 target_genotype = 'Aabb'):
    
    target = list()
    
    for i in range(0, len(parent1), 2):
        target.append((target_genotype[i], target_genotype[i+1]))

    all_genotypes = []
    for i in range(0, len(parent1), 2):
        genotype = []
        for el in itertools.product(parent1[i:i+2], parent2[i:i+2]):
            genotype.append(tuple(sorted(list(el))))
        all_genotypes.append(genotype)
    
    p = 1
    for n , allele in enumerate(target):
        p *= all_genotypes[n].count(allele) / len(all_genotypes[n])
        
    return p


# In[28]:


probability_genotype()


# ### 3.

# ## Do not run this code (32 min on 32GB, 16GB and 8GB RAM )

# In[29]:


def all_genotypes_find(parent1, parent2, to_find, file_to_record):
    
    all_genotypes = []
    for i in range(0, len(parent1), 2):
        genotype = []
        for el in itertools.product(parent1[i:i+2], parent2[i:i+2]):
            genotype.append(sorted(list(el)))
        all_genotypes.append(genotype)
    
    with open(file_to_record, 'a') as file:
        for combination in itertools.product(*all_genotypes):
                patially_joined = map(lambda x: ''.join(x), combination)
                fully_joined = ''.join(patially_joined)
                if to_find in fully_joined:
                    print(fully_joined, file=file)


# In[30]:


all_genotypes_find(parent1='АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн', parent2='АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН', 
                   to_find='АаБбВвГгДдЕеЖжЗзИиЙйКкЛл',file_to_record='../data/genotypes_brute_force')


# #### Run this code instead (sorry, but maybe it implements too much mathematics )

# In[37]:


def tricky_finder(parent1, parent2, to_find, file_to_record):
    
    target = list()
    
    for i in range(0, len(to_find), 2):
        target.append([to_find[i], to_find[i+1]])
    
    all_genotypes = []
    for i in range(0, len(parent1), 2):
        genotype = []
        for el in itertools.product(parent1[i:i+2], parent2[i:i+2]):
            genotype.append(sorted(list(el)))
        all_genotypes.append(genotype)
    
    new_all_genotypes = []
    
    for n in range(len(all_genotypes)):
        new_all_genotypes.append(all_genotypes[n].copy())
    
    for n, allele in enumerate(target):
        for variant in all_genotypes[n]:
            if allele != variant:
                new_all_genotypes[n].remove(variant)
    
    with open(file_to_record, 'a') as file:
        for combination in itertools.product(*new_all_genotypes):
                patially_joined = map(lambda x: ''.join(x), combination)
                print(''.join(patially_joined), file=file)


# In[38]:


tricky_finder(parent1='АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн', 
              parent2='АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН', 
              to_find='АаБбВвГгДдЕеЖжЗзИиЙйКкЛл',
              file_to_record = '../data/genotypes_tricky.txt')


# ### 4.

# In[33]:


probability_genotype(parent1="АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн", parent2="АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн", 
                 target_genotype = 'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн')

