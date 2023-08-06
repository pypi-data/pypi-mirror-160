"""Functions to manipulate an Annotation Lab JSON export into an appropriate layout for training
assertion, relation extraction and NER models
"""
import itertools
import json
import os

import pandas as pd
from .sparknlp_jsl.utils.alab_utils import get_nlp_token_pipeline, get_nlp_regex_token_pipeline, get_rel_df, \
    get_ner_sentence_borders, get_single_task_conll


def get_assertion_data(spark, input_json_path, assertion_labels, relevant_ner_labels, ground_truth=False,
                       unannotated_label=None, regex_pattern=None):
    """Generate a dataframe to train assertion models in Spark NLP from an Annotation Lab JSON export

    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param assertion_labels: annotated assertion labels to train on
    :type assertion_labels: list
    :param relevant_ner_labels: relevant NER labels that are assigned assertion labels
    :type relevant_ner_labels: list
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param unannotated_label: assertion label to assign to entities that have no assertion, defaults to None
    :type unannotated_label: str
    :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
    :type regex_pattern: str
    :return: dataframe in appropriate layout for training assertion models
    :rtype: pd.DataFrame
    """

    if regex_pattern is not None:
        lp_pipeline = get_nlp_regex_token_pipeline(spark=spark, regex_pattern=regex_pattern)

    elif regex_pattern is None:
        lp_pipeline = get_nlp_token_pipeline(spark=spark)

    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        output_list = json.load(json_file)

    ner_dicts = []
    for w, output in enumerate(output_list):
        try:
            text = output['data']['text']
            if ground_truth:
                for i in range(len(output['completions'])):
                    if output['completions'][i]['honeypot']:
                        gt_index = i

            elif ground_truth is False or ground_truth is None:
                gt_index = -1

            doc_id = output['completions'][gt_index]['id']

        except:
            print('EXCEPTION:', input_json_path.split('/')[-1], 'Task ID#', output['id'])
            continue

        lines = [(line.result, line.begin, line.end) for line in lp_pipeline.fullAnnotate(text)[0]['sentence']]

        sent_df = pd.DataFrame(lines, columns=['sentence', 'begin', 'end'])

        try:
            for _, i in enumerate(output['completions'][gt_index]['result']):

                if i['type'] == 'labels':
                    assertion_label = i['value']['labels'][0]

                    sentence = sent_df[(i['value']['start'] >= sent_df.begin) &
                                       (i['value']['start'] <= sent_df.end) &
                                       (i['value']['end'] - 1 >= sent_df.begin) &
                                       (i['value']['end'] - 1 <= sent_df.end)]

                    if len(sentence) == 0:
                        continue

                    sent = sentence['sentence'].values[0]

                    begin = i['value']['start'] - sentence['begin'].values[0]
                    end = i['value']['end'] - sentence['begin'].values[0]

                    token_lines = [(line.result, line.begin, line.end) for line in
                                   lp_pipeline.fullAnnotate(sent)[0]['token']]

                    token_df = pd.DataFrame(token_lines, columns=['token', 'begin', 'end'])

                    ix = token_df[(token_df.begin >= begin) & (token_df.end < end)].index

                    if len(ix) == 0:
                        continue
                    left_ix = min(ix)
                    right_ix = max(ix)

                    ner_dicts.append((doc_id, sent, i['value']['text'], assertion_label, left_ix, right_ix,
                                      i['value']['start'], i['value']['end']))

        except:
            print('EXCEPTION:', input_json_path.split('/')[-1], 'Task ID#', output['id'])
            continue

        print('Processing Task ID#', w)

    ass_df = pd.DataFrame(ner_dicts,
                          columns=['task_id', 'text', 'target', 'label', 'start', 'end', 'doc_start_index',
                                   'doc_end_index'])
    ass_df["json_file_path"] = input_json_path

    relevant_ner_df = ass_df[ass_df['label'].isin(relevant_ner_labels)]
    relevant_ass_df = ass_df[ass_df['label'].isin(assertion_labels)]

    ass_inner_duplicates = relevant_ass_df.merge(relevant_ner_df,
                                                 on=['task_id', 'text', 'target', 'start', 'end', 'doc_start_index',
                                                     'doc_end_index', 'json_file_path'], how='inner').drop(
        columns='label_y').rename(columns={'label_x': 'label'})

    if unannotated_label is not None:
        ass_outer_duplicates = relevant_ass_df.merge(relevant_ner_df,
                                                     on=['task_id', 'text', 'target', 'start', 'end', 'doc_start_index',
                                                         'doc_end_index', 'json_file_path'], how='right',
                                                     indicator=True).query('_merge == "right_only"').drop(
            columns=['_merge', 'label_y']).rename(columns={'label_x': 'label'})
        ass_outer_duplicates['label'] = unannotated_label
        ass_df = pd.concat([ass_inner_duplicates, ass_outer_duplicates]).reset_index(drop=True)
        ass_df = ass_df.sort_values(['task_id', 'doc_start_index', 'doc_end_index']).reset_index(drop=True)

    else:
        ass_df = ass_inner_duplicates.copy()
        ass_df = ass_df.sort_values(['task_id', 'doc_start_index', 'doc_end_index']).reset_index(drop=True)

    ass_df = ass_df[['text', 'target', 'label', 'start', 'end']]

    return ass_df


def get_relation_extraction_data(spark, input_json_path, ground_truth=False, negative_relations=False,
                                 assertion_labels=None, relation_pairs=None):
    """Generate a dataframe to train relation extraction models in Spark NLP from an Annotation Lab JSON export

    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param negative_relations: set to True to assign a relation label between entities where no relation was
    annotated, defaults to False
    :type negative_relations: bool
    :param assertion_labels: all assertion labels that were annotated, defaults to None
    :type assertion_labels: list
    :param relation_pairs: plausible pairs of entities for relations, separated by a `-`, use the same casing as
    the annotations, include only one relation direction, defaults to all possible pairs of annotated entities
    :type relation_pairs: list
    :return: dataframe in appropriate layout for training relation extraction models
    :rtype: pd.DataFrame
    """

    rel_df = get_rel_df(input_json_path=input_json_path, ground_truth=ground_truth)
    ner_borders_df = get_ner_sentence_borders(spark=spark, input_json_path=input_json_path, ground_truth=ground_truth,
                                              assertion_labels=assertion_labels)

    official_rel_df_col_names = ["sentence", "firstCharEnt1", "firstCharEnt2", "lastCharEnt1", "lastCharEnt2",
                                 "chunk1", "chunk2", "label1", "label2", "rel"]
    full_rel_df = rel_df.merge(ner_borders_df.add_prefix('from_'), left_on='from_id',
                               right_on='from_chunk_id').merge(ner_borders_df.add_prefix('to_'), left_on='to_id',
                                                               right_on='to_chunk_id')

    if negative_relations:
        group_df = ner_borders_df.groupby(['ner_sentence_id', 'ner_sentence'])

        new_relations_list = []
        text_list = []
        ner_label_list = []
        text_indexes_list = []
        sentence_list = []

        ind = 0
        for key, _ in group_df:
            ind += 1
            a_group = group_df.get_group(key)
            a_group = a_group.sort_values(by='sentence_begin')
            x = a_group['ner_label'].values
            y = a_group['text'].values
            ch = a_group['chunk_id'].values
            z = a_group['ner_sentence'].values
            s_e = a_group[['start', 'end']].values
            ner_se = a_group[['ner_sentence_start_border', 'ner_sentence_end_border']].values
            s_be = a_group[['sentence_begin', 'sentence_end']].values

            text_indexes = list(zip(s_e, ner_se, s_be))
            id_w_indexes = list(zip(ch, text_indexes))

            new_relations_list.extend(list(itertools.combinations(ch, 2)))
            text_list.extend(list(itertools.combinations(y, 2)))
            ner_label_list.extend(list(itertools.combinations(x, 2)))
            text_indexes_list.extend(list(itertools.combinations(id_w_indexes, 2)))
            sentence_list.extend(itertools.repeat(z, len(list(itertools.combinations(y, 2)))))

        new_relations_df = pd.DataFrame(new_relations_list, columns=['from_id', 'to_id'])
        new_relations_df['id_pairs'] = new_relations_df.apply(lambda k: (k['from_id'], k['to_id']), axis=1)
        new_relations_df['sentence'] = sentence_list
        new_relations_df['sentence'] = new_relations_df['sentence'].apply(lambda t: t[0])
        new_relations_df['from_start'] = [i[0][1][2][0] for i in text_indexes_list]
        new_relations_df['to_start'] = [i[1][1][2][0] for i in text_indexes_list]
        new_relations_df['from_end'] = [i[0][1][2][1] for i in text_indexes_list]
        new_relations_df['to_end'] = [i[1][1][2][1] for i in text_indexes_list]
        new_relations_df['from_text'] = [i[0] for i in text_list]
        new_relations_df['to_text'] = [i[1] for i in text_list]
        new_relations_df['from_ner_label'] = [i[0] for i in ner_label_list]
        new_relations_df['to_ner_label'] = [i[1] for i in ner_label_list]
        new_relations_df['relation'] = 'O'

        existing_rel_ids = list(zip(full_rel_df['from_id'], full_rel_df['to_id']))
        existing_rel_ids_reverse = [t[::-1] for t in existing_rel_ids]
        existing_rel_ids_all = existing_rel_ids + existing_rel_ids_reverse
        new_relations_df = new_relations_df[
            [x not in existing_rel_ids_all for x in zip(new_relations_df.from_id, new_relations_df.to_id)]]

        new_relations_df = new_relations_df[
            ['sentence', 'from_start', 'to_start', 'from_end', 'to_end', 'from_text', 'to_text', 'from_ner_label',
             'to_ner_label', 'relation']]
        full_rel_df = full_rel_df[
            ['from_ner_sentence', 'from_sentence_begin', 'to_sentence_begin', 'from_sentence_end',
             'to_sentence_end', 'from_text', 'to_text', 'from_ner_label', 'to_ner_label', 'relation']]
        new_relations_df.columns = official_rel_df_col_names
        full_rel_df.columns = official_rel_df_col_names
        final_rel_df = pd.concat([full_rel_df, new_relations_df]).reset_index(drop=True)

    else:
        full_rel_df = full_rel_df[
            ['from_ner_sentence', 'from_sentence_begin', 'to_sentence_begin', 'from_sentence_end',
             'to_sentence_end', 'from_text', 'to_text', 'from_ner_label', 'to_ner_label', 'relation']]
        full_rel_df.columns = official_rel_df_col_names
        final_rel_df = full_rel_df.copy()

    if relation_pairs is not None:
        user_input_rel_pairs = [(i.split('-')[0], i.split('-')[1]) for i in relation_pairs]
        user_input_rel_pairs_reverse = [t[::-1] for t in user_input_rel_pairs]
        candidate_rel_pairs = user_input_rel_pairs + user_input_rel_pairs_reverse
        final_rel_df = final_rel_df[
            [x in candidate_rel_pairs for x in zip(final_rel_df.label1, final_rel_df.label2)]]

    reorder = final_rel_df['firstCharEnt1'] > final_rel_df['firstCharEnt2']

    final_rel_df.loc[reorder, ['firstCharEnt1', 'firstCharEnt2', 'lastCharEnt1', 'lastCharEnt2',
                               'chunk1', 'chunk2', 'label1', 'label2']] = (
        final_rel_df.loc[reorder, ['firstCharEnt2', 'firstCharEnt1', 'lastCharEnt2', 'lastCharEnt1',
                                   'chunk2', 'chunk1', 'label2', 'label1']].values)

    final_rel_df = final_rel_df.reset_index(drop=True)
    return final_rel_df


def get_conll_data(spark, input_json_path, output_name, save_dir='exported_conll', ground_truth=False,
                   excluded_labels=None, excluded_docs=None, regex_pattern=None):
    """Generates a CoNLL file from an Annotation Lab JSON export

    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param output_name: name of the CoNLL file to save
    :type output_name: str
    :param save_dir: path for CoNLL file saving directory, defaults to 'exported_conll'
    :type save_dir: str
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param excluded_labels: labels to exclude from CoNLL; these are all assertion labels and irrelevant NER labels,
    defaults to empty list
    :type excluded_labels: list
    :param excluded_docs: Annotation Lab task titles to exclude from CoNLL, defaults to empty list
    :type excluded_docs: list
    :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
    :type regex_pattern: str
    :return: CoNLL file
    :rtype: io.TextIOWrapper
    """
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        json_outputs = json.load(json_file)

    bulk_conll_lines = ["-DOCSTART- -X- -X- O\n\n"]

    for _, output in enumerate(json_outputs):
        in_conll_lines = get_single_task_conll(spark=spark, output=output, ground_truth=ground_truth,
                                               excluded_labels=excluded_labels, excluded_docs=excluded_docs,
                                               regex_pattern=regex_pattern)
        bulk_conll_lines.extend(in_conll_lines)

    try:
        os.mkdir(save_dir)
    except:
        pass

    with open(f'{save_dir}/{output_name}.conll', 'w', encoding='utf-8') as f:
        for i in bulk_conll_lines:
            f.write(i)

    print(f'{save_dir}/{output_name}.conll')

    return bulk_conll_lines
