
import numpy as np
import re

""" SurveyHumpbackWhale is a module with the purpouse of automatize tasks in order to proccess survey's data easily.

This module mainly transform the answers into numbers in order of aplying learning algorithms like clustering or
random forests. Also it has some functions that correct errors in surveys or combine the free comments columns
with electable answers included, in example, in a survey with a question of the most used apps, we can include
answers and a free comment answer where the user writes what he want. This function module can combine this 
free question with the tipo question that are included in the survey.

    Typical usage example:
        
    import SurveyHumpbackWhale as surv_whale
    import pandas as pd
    
    dataset_survey = pd.read_csv(path, separator=',')
    comment_columns = surv_whale.comment_columns_detector(dataset_survey) # Detects comment columns.
    surv_whale.aglutinate_comment_columns(dataset_survey, comment_columns) # Combine the comment columns with survey tipo answers.
"""

# Regular expressions to make transforms in the data
_re_words_finder        = re.compile(r"[a-zA-ZáéíóúÁÉÍÓÚ]*")
_re_comment_pattern     = re.compile(r"-COMENTARIO-|-COMMENT-")
_re_digit_pattern       = re.compile(r"[\d|\d\.]*")
_re_zero_pattern        = re.compile(r"ningún|solo|ninguno|ninguna|nadie|no recuerdo|no lo sé|desconozco|only|no one|i don't remember|i do not remember|i don't know|i do not know|alone|no")
_re_afirmative_pattern  = re.compile(r"yes")
_re_error_pattern       = re.compile(r"aaa Not A Number aaa")
_re_other_pattern       = re.compile(r"other")
    

# Corpus of language particles

corpus_lang_particles = {'Greater_particles':['más', 'more', 'with more', 'up to'], 
                         'Middle_particles':['entre', 'between', 'de', 'from'], 
                         'Lesser_particles':['menos','less', 'hasta', 'with less'],
                         'Zero_particles':["ningún","solo","ninguno","ninguna","nadie",
                                           "no sé",
                                           "no recuerdo","no lo sé","desconozco","only",
                                           "no one","i don't remember","i do not remember",
                                           "i don't know","i do not know","i live alone","no"],
                         'Afirmative_particles':['yes'],
                         'Error_particles':['nan'],
                         'Temporal_particles':{
                             'spanish': ['siempre', 'habitualmente', 'a veces', 'nunca'],
                             'english': ['always', 'daily', 'normally', 'several times', 'sometimes', 'never', 'twice', 'once', 'year', 'week', 'day', 'None']
                             },
                         'Quantifiers':['none', 'primary', 'secondary', 'higher']
                         }

def list_to_num_dict(list_elements):
    """Converses a list to dictionary keeping the order of the list.
    
    Converses a list to dictionary keeping the order of the list.
    
    Args:
        list_elements: A list of elements that can be any type.
    
    Returns:
        A dictionary with every element of the input list keeping its order.
    """

    dictionary = {}
    
    for element in list_elements:
        try:
            element = int(element)
            dictionary[element] = element
        except ValueError:
            if type(element) == type(""): 
                if element.lower() in corpus_lang_particles['Zero_particles']:
                        dictionary[element] = 0
                        
                else:
                    dictionary[element] = len(dictionary)
            else:
                dictionary[element] = len(dictionary)

    return dictionary

def map_answers_to_categories(dataset):
    
    """Maps survey answers in a dataset to a dictionary in order of transform to numbers later.
    
    Maps every answer to the survey recollected in the dataset in order of transform all of
    that to ordinal variables. Also it takes in consideration important language quantifiers
    like 'Between' or 'More' to make this kind of permutations.
    
    Args:
        dataset: A dataset divided in columns and rows, like DataFrame from pandas module.
        
    Returns:
        A dict that map every answer (dataset value in column j and row i) to every question
        of the survey (dataset column name). For example:
            
        For a dataset like this:        
        
        dataset = pd.DataFrame(data = {'Do you like this python module?': ['Yes', 'No'], 
                                       'How useful do you thing it is from 1 to 10?': [3, 8]})
        
        This function returns a dict like this:
            
        dict_data = {0: {'question':'Do you like this python module?', 'answers':{'No':0, 'Yes':1}}
                     1: {'question':'How useful do you thing it is from 1 to 10?', 'answers':{'3':3, '8':8}}}
    """

    answers_key_value = {} # Dict to store the survey structure.
    answers_map_to_replace_in_dataframe = {} # Dict to directly replace in a pandas dataframes the natural values for the new digit values
    
    columns_data    = dataset.columns # Columns of dataset (as known as survey questions).
    
    for index, column in enumerate(columns_data):
        answers = list(dataset[column].unique()) # Take all kind of the answers giving to the question and converts it in a list.
        
        # Now we try to remove the nan data that can be in the survey and 
        # replace it by a string that can be manipulate easily. It can raise
        # a ValueError exception if there isn't a nan value in the answers, in
        # that case nothing needs to be changed.
        
        try: 
            answers.remove(np.nan)
            answers.append('nan')
            
        except ValueError:
            pass
        
        # In this part we look if there are some language particle that
        # denotates the existence of a range of values, in case that we find
        # words like 'Between' or 'More', we proceed to make an smart sort of
        # answers. Otherwise, we just orther the answers alphabetically. If 
        # all the answers are numbers, it can raises a TypeError and then 
        # just need to sort the answers.
        
        try:                
            if(len(_re_words_finder.findall(answers[0])) >= 3):
                                
                if (('{} {}'.format(_re_words_finder.findall(answers[0])[0].lower(),
                                    _re_words_finder.findall(answers[0])[2].lower())) 
                                in corpus_lang_particles['Greater_particles'] or
                                
                    ('{} {}'.format(_re_words_finder.findall(answers[0])[0].lower(),
                                    _re_words_finder.findall(answers[0])[2].lower())) 
                                in corpus_lang_particles['Middle_particles'] or
                    
                    ('{} {}'.format(_re_words_finder.findall(answers[0])[0].lower(),
                                    _re_words_finder.findall(answers[0])[2].lower())) 
                                in corpus_lang_particles['Lesser_particles'] or
                                
                     ('{} {}'.format(_re_words_finder.findall(answers[0])[0].lower(),
                                    _re_words_finder.findall(answers[0])[2].lower())) 
                                in corpus_lang_particles['Temporal_particles']['english']):
                
                    answers = smart_answers_sort(answers)
                    
                elif (_re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Greater_particles'] or 
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Middle_particles'] or 
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Lesser_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Zero_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Afirmative_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Temporal_particles']['spanish'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Temporal_particles']['english'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Quantifiers']):
                    
                    answers = smart_answers_sort(answers)
                
                elif (answers[0].lower() in corpus_lang_particles['Greater_particles'] or 
                    answers[0].lower() in corpus_lang_particles['Middle_particles'] or 
                    answers[0].lower() in corpus_lang_particles['Lesser_particles'] or
                    answers[0].lower() in corpus_lang_particles['Zero_particles'] or
                    answers[0].lower() in corpus_lang_particles['Afirmative_particles'] or
                    answers[0].lower() in corpus_lang_particles['Temporal_particles']['spanish'] or
                    answers[0].lower() in corpus_lang_particles['Temporal_particles']['english']or
                    answers[0].lower() in corpus_lang_particles['Quantifiers']):
                                        
                    answers = smart_answers_sort(answers)
                
                else: 
                    answers.sort()
            
            elif (len(_re_words_finder.findall(answers[0])) < 3):
                                
                if (_re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Greater_particles'] or 
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Middle_particles'] or 
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Lesser_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Zero_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Afirmative_particles'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Temporal_particles']['spanish'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Temporal_particles']['english'] or
                    _re_words_finder.findall(answers[0])[0].lower() in corpus_lang_particles['Quantifiers']):
                    
                    answers = smart_answers_sort(answers)
                
            else: 
                
                answers.sort()
                
            
        except TypeError or IndexError:
            answers.sort()
        
        # Finally we add to the dictionary that has all the questions, answers and its
        # transformation to number the dictionary with the question (column) and the 
        # dictionary of all the answers finded, created by an auxiliar function.
        
        answers_key_value[index] = {'question':column, 'answers': list_to_num_dict(answers)}    
        answers_map_to_replace_in_dataframe[index] = {column : list_to_num_dict(answers)}    

    return answers_key_value, answers_map_to_replace_in_dataframe

def make_new_columns_from_answers(dataset, columns_to_look_at):
    """Makes new columns based on the answers giving to the survey.
    
    Makes new columns based on the answers giving to the survey, this function
    obtain the new columns to create in order of extend a certain columns
    from a dataset.
    
    Args:
        dataset: A dataset divided in columns and rows, like DataFrame from 
                pandas module that needs to be traduced.
        columns_to_look_at: A list of numbers that represent the index of the
                            columns to extend
            
    Returns:
        A list with the names of the new extended columns.
    """
    
    new_columns = []
    for column in columns_to_look_at:
        for value in dataset[dataset.columns[column]].unique():
            try:
                aux = value.replace("[", "").replace("]", "")
                
                for new_column in aux.split(","):
                    
                    if new_column[0] == " ":
                        aux_new_column = new_column[1:]
                    else:
                        aux_new_column = new_column
            
                    if aux_new_column != 'other':
                        
                        if aux_new_column == 'Ninguno' or aux_new_column == 'Ninguna' or aux_new_column == 'Nimguno' or aux_new_column == 'Nimguna':
                            aux_new_column = '{}_Ninguno'.format(dataset.columns[column])

                        else:
                            aux_new_column = '{}_{}'.format(dataset.columns[column], aux_new_column.replace(' ','_'))
                 
                        if aux_new_column not in new_columns:
                            new_columns.append(aux_new_column)
                    
            except AttributeError:
                pass           
            
            
    return new_columns


# Fix section
    
def combine_comment_columns(dataset, columns_to_look_at, re_other_pattern = _re_other_pattern):
    
    """Combines the free answer columns with the pre-writed answers column.
    
    Combines the free answer columns with the pre-writed answers column (ie: 
    'What is the app that you use most of the time?' and the answers were 
    'whatsapp', 'facebook' or 'other', where when you mark 'other' enable an 
    input of text to write). 
        
    Args:
        dataset: A dataset divided in columns and rows, like DataFrame from 
                pandas module.
        columns_to_look_at: A list that contains the comment column's index.
        re_other_pattern: A regular expression the identifies the word that 
                        enables a free input of text in a survey. By default
                        its setup to the word 'other'.
                        
    Returns:
        Void, just updates the dataset introduce by parameter.
    """

    for column in columns_to_look_at:
        
        for row_index in range(len(dataset)):            
            if re_other_pattern.search(str(dataset.iloc[row_index, column - 1])):
                phrase      = str(dataset.iloc[row_index, column - 1])
                location    = re_other_pattern.search(phrase)
                
                if phrase[0:location.start()] + phrase[location.end():] != '':
                    dataset.iloc[row_index, column - 1] = phrase[0:location.start()] + " " + dataset.iloc[row_index, column] + " " + phrase[location.end():]
                
                else:
                    dataset.iloc[row_index, column - 1] = dataset.iloc[row_index, column]
                
            
            elif re_other_pattern.search(str(dataset.iloc[row_index, column + 1])):
                phrase      = str(dataset.iloc[row_index, column + 1])
                location    = re_other_pattern.search(phrase)
                
                if phrase[0:location.start()] + phrase[location.end():] != '':
                    dataset.iloc[row_index, column + 1] = phrase[0:location.start()] + " " + dataset.iloc[row_index, column] + " " + phrase[location.end():]
                
                else:
                    dataset.iloc[row_index, column + 1] = dataset.iloc[row_index, column]
                                        
def fix_date_format(df, columns_with_dates):
    
    for column in columns_with_dates:
        aux = df[column].str.contains('[0-9]*\.[0-9]*\.[0-9]*')
        
    return aux

def smart_answers_sort(answers_list):
    
    """Sorts the answers from a survey stored in a dataframe.
    
    Sorts the answers from a survey stored in a dataframe in consideration
    of the answer represents a range by locating language particles that has 
    implicit meaning of range (ie: 'Between' or 'Less ... than').
    
    Args:
        answers_list: A list with the answers that can had a meaning of range.
        
    Returns:
        A list that contains all the answers from answers_list but ordered in
        function of the ranges that represents.
    """
    
    answers_examples = {}
    answer_not_numeric = 0
    
    for element in answers_list:
        
        # First, we extract the numeric elements and word elements from an 
        # answer throught the regular expressions defined at the begining of
        # the module. 
        
        digit_list = _re_digit_pattern.findall(element)
        clean_digit_list = list(filter(None, digit_list))
        
        words_list = _re_words_finder.findall(element)
        clean_words_list = list(filter(None, words_list))
        
        # Then we make a transform in the numeric elements converting it to 
        # python format. This is because the number format from the surveys 
        # (ie: 2.000 or 1,23 in survey and 2000 or 1.23 in python).

        clean_digit_list = smart_digit_conversion(clean_digit_list)        
    
        # Checks if the answer is contextually null (ie: for question, 'How 
        # many people live with you?, the answer 'alone' it's equivalent to 0).
        
        if clean_words_list[0].lower() in corpus_lang_particles['Zero_particles']:
            answers_examples[answers_list.index(element)] = 0
        
        elif combine_all_words(clean_words_list).lower() in corpus_lang_particles['Zero_particles']:
            answers_examples[answers_list.index(element)] = 0
            
        elif clean_words_list[0].lower() in corpus_lang_particles['Afirmative_particles']:
            answers_examples[answers_list.index(element)] = 1           

        else:
            
            # Identifies the kind of particle with the corpus of particles defined at
            # the begin of the module and took a represent of the range in function of
            # the particle. First looking the len of the answer, then apply the kind of
            # preprocess adecuated to it.
            
            if (len(clean_words_list) >= 2):
                if (clean_words_list[0].lower() in corpus_lang_particles['Greater_particles'] or
                    ("{} {}".format(clean_words_list[0].lower(), clean_words_list[1].lower()) in corpus_lang_particles['Greater_particles'])):
                    answers_examples[answers_list.index(element)] = clean_digit_list[0] + 1
    
                elif (clean_words_list[0].lower() in corpus_lang_particles['Middle_particles']):
                    answers_examples[answers_list.index(element)] = (clean_digit_list[0] + clean_digit_list[1]) / 2
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Lesser_particles'] or
                    ("{} {}".format(clean_words_list[0].lower(), clean_words_list[1].lower()) in corpus_lang_particles['Lesser_particles'])):
                    answers_examples[answers_list.index(element)] = clean_digit_list[0] - 1
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Temporal_particles']['english'] or
                    ("{} {}".format(clean_words_list[0].lower(), clean_words_list[1].lower()) in corpus_lang_particles['Temporal_particles']['english'])):
                    try:
                        answers_examples[answers_list.index(element)] = len(corpus_lang_particles['Temporal_particles']['english']) - corpus_lang_particles['Temporal_particles']['english'].index(clean_words_list[0].lower())
                    
                    except ValueError:
                        auxiliar_element = "{} {}".format(clean_words_list[0].lower(), clean_words_list[1].lower())
                        answers_examples[answers_list.index(element)] = len(corpus_lang_particles['Temporal_particles']['english']) - corpus_lang_particles['Temporal_particles']['english'].index(auxiliar_element)
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Quantifiers']):
                    answers_examples[answers_list.index(element)] = corpus_lang_particles['Quantifiers'].index(clean_words_list[0].lower())
                
            else:
                if (clean_words_list[0].lower() in corpus_lang_particles['Greater_particles']):
                    answers_examples[answers_list.index(element)] = clean_digit_list[0] + 1
    
                elif (clean_words_list[0].lower() in corpus_lang_particles['Middle_particles']):
                    answers_examples[answers_list.index(element)] = (clean_digit_list[0] + clean_digit_list[1]) / 2
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Lesser_particles']):
                    answers_examples[answers_list.index(element)] = clean_digit_list[0] - 1
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Temporal_particles']['english']):
                    answers_examples[answers_list.index(element)] = len(corpus_lang_particles['Temporal_particles']['english']) - corpus_lang_particles['Temporal_particles']['english'].index(clean_words_list[0].lower())
                
                elif (clean_words_list[0].lower() in corpus_lang_particles['Quantifiers']):
                    answers_examples[answers_list.index(element)] = corpus_lang_particles['Quantifiers'].index(clean_words_list[0].lower())
    
            
    # Finally, we acummulated the answers with the 'represent' of its range and
    # we sort them.                
    
    answers_examples_def = {k: v for k, v in sorted(answers_examples.items(), key=lambda item: item[1])}

    definitive_answers_list = []
    
    for answer in list(answers_examples_def.keys()):            
        definitive_answers_list.append(answers_list[answer])
        
    return definitive_answers_list

def smart_digit_conversion(digit_list):
    
    """Converts the survey number format to python number format
    
    Converts the numeric answers from a survey like 2.000 or 1,23; to the 
    python number format like 2000 or 1.23 in order of evade errors.
    
    Args:
        digit_list: A list of the digits to be converse.
        
    Returns:
        A new digit list in the python numeric format.
    """
    
    new_digit_list = []
    
    for digit in digit_list:
        if digit.find('.') != -1:
            new_digit = digit.replace('.','')
            new_digit_list.append(int(new_digit))
        elif digit.find(',')  != -1:
            new_digit = digit.replace(',','.')
            new_digit_list.append(float(new_digit))
        
        else:
            new_digit_list.append(int(digit))

    return new_digit_list

def traduce_survey_with_dictionary(dict_traduction, dataset):
    
    
    
    """Traduces a survey answers dataframe with a dictionary.
    
    Traduces the dataframe that represents questions and answers from a survey
    in function of a dictionary which key represents the non traduce part of
    the dataset and value represents the traduction. Sometimes its useful to
    make multilangual surveys and this function helps to mix various sources
    of data.
    
    Args: 
        dict_traduction: Dictionary who directs the traduction process. Keys 
                        are the value that needs to be traduced and values are
                        its traduction.
        dataset: A dataset divided in columns and rows, like DataFrame from 
                pandas module that needs to be traduced.
        
    Returns:
        A new dataframe completly traduced.
    """
    
    dataset_to_work = dataset.copy()
    
    for key in list(dict_traduction.keys()):
        
        key_to_search = key.replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
        dataset_to_work = dataset_to_work.replace(to_replace=key_to_search, value=dict_traduction[key],regex=True)
        
        
    return dataset_to_work

def comment_columns_detector(dataset, comment_columns_pattern = _re_comment_pattern):
    
    """Detects comment columns.
    
    Detects the columns where is stored the input from free answers (ie: 
    'What is the app that you use most of the time?' and the answers were 
    'whatsapp', 'facebook' or 'other', where when you mark 'other' enable an 
    input of text to write and the columns that contains that answers is what
    is finded with this method).
        
    Args:
        dataset: A dataset divided in columns and rows, like DataFrame from 
                pandas module.
        comment_columns_pattern: A regular expression the identifies the word 
                                used for this kind of columns in a survey. By
                                default its setup to the word '-COMENTARIO-' 
                                or '-COMMENT-'.
    Returns: 
        A list of the detected comment column's index by the pattern inside
        of the dataset.
    """
    columns_list = list(dataset.columns)
    comment_columns = []
    columns_to_look_at = []
    
    
    for column_index, column_name in enumerate(columns_list):
        if comment_columns_pattern.search(column_name):
            comment_columns.append(column_index)
            columns_to_look_at.append(column_index)
        
    return comment_columns
    
def create_and_poblate_new_columns(dataset, new_columns):
    
    """Creates and poblates with the new columns the input dataset.
    
    Creates and poblates with the new columns the input dataset that 
    represent the survey, in example, in a survey with a question of the most 
    used apps and answers like: 'whatsapp', 'facebook' or 'instagram' and we 
    want to make a new column that marks people who used mostly facebook this
    function create the column and marks to 1 or 0 depending if it was
    the answer selected.
    
    Args:
        dataset: A dataset divided in columns and rows, like DataFrame from 
                pandas module.
        new_columns: A list of the new extended columns.
    
    Returns:
        Void, just updates the dataset introduce by parameter.        
    """
    
    for column in new_columns:
        base_column = column.split('_')[0]
        new_name_column = ' '.join(column.split('_')[1:])
        dataset[column] = 0    

        new_columns_index = list(dataset.columns).index(column)
        to_find = new_name_column.replace('(', '\(').replace(')', '\)').replace('.', '\.')

        while to_find[0] == ' ':
            to_find = to_find[1:]
            
        while to_find[len(to_find)-1] == ' ':
            to_find = to_find[:len(to_find)-1]
    
        rastreator = re.compile(r"{}".format(to_find.lower()))
        
        for index_row, row in enumerate(dataset[base_column]):
                
            if (type(row) == str):
                
                if re.search(rastreator, row.lower()):   
                    dataset.iloc[index_row:index_row+1, new_columns_index] = 1
        
        
    for column in new_columns:
        base_column = column.split('_')[0]
        
        if base_column in list(dataset.columns): 
            dataset = dataset.drop([base_column], axis=1)
            
            
def combine_all_words(list_of_words):
    aux = ""
    for i, word in enumerate(list_of_words):
        if i == 0:
            aux = word
        else:
            aux += " {}".format(word)
            
    return aux