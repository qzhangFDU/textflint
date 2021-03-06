r"""
MRC Generator Class
============================================

"""
__all__ = ['MRCGenerator']
from .generator import Generator
from tqdm import tqdm
from ...common.utils.logger import logger
from ...common.utils import load_supporting_file
from ...common.settings import NEAR_DICT_PATH, POS_DICT_PATH
from ...common.utils.install import download_if_needed
from ...common.settings import TASK_TRANSFORMATION_PATH, \
    ALLOWED_TRANSFORMATIONS, TASK_SUBPOPULATION_PATH, ALLOWED_SUBPOPULATIONS


class MRCGenerator(Generator):

    def __init__(
        self,
        task='MRC',
        max_trans=1,
        fields='context',
        transformation_methods=None,
        transformation_config=None,
        return_unk=True,
        subpopulation_methods=None,
        subpopulation_config=None,
        attack_methods=None,
        validate_methods=None,
    ):
        super().__init__(
            task=task,
            max_trans=max_trans,
            fields=fields,
            transformation_methods=transformation_methods,
            transformation_config=transformation_config,
            return_unk=return_unk,
            subpopulation_methods=subpopulation_methods,
            subpopulation_config=subpopulation_config,
            attack_methods=attack_methods,
            validate_methods=validate_methods
        )

        self.nearby_word_dict, self.pos_tag_dict = load_supporting_file(
            download_if_needed(NEAR_DICT_PATH),
            download_if_needed(POS_DICT_PATH))

    @staticmethod
    def sample_filter(samples, type):

        if 'Case-upper' in type or 'Case-lower' in type or 'Case-title' in type:
            for sample in samples:
                for answer in sample.answers:
                    if 'Case-upper' in type:
                        answer['text'] = answer['text'].upper()
                    elif 'Case-lower' in type:
                        answer['text'] = answer['text'].lower()
                    else:
                        answer['text'] = answer['text'].title()

        return samples

    def generate_by_transformations(self, dataset, **kwargs):
        self.prepare(dataset)

        for trans_obj in self._get_flint_objs(
            self.transform_methods,
            TASK_TRANSFORMATION_PATH,
            ALLOWED_TRANSFORMATIONS
        ):
            # initialize current index of dataset
            dataset.init_iter()

            logger.info('******Start {0}!******'.format(trans_obj))
            generated_samples = dataset.new_dataset()
            original_samples = dataset.new_dataset()

            for sample in tqdm(dataset):
                # default return list of samples
                trans_rst = trans_obj.transform(
                    sample, n=self.max_trans, field=self.fields,
                    nearby_word_dict=self.nearby_word_dict,
                    pos_tag_dict=self.pos_tag_dict
                )
                trans_rst = self.sample_filter(trans_rst, trans_obj.__repr__())
                if trans_rst:
                    generated_samples.extend(trans_rst)
                    original_samples.append(sample)

            yield original_samples, generated_samples, trans_obj.__repr__()
            logger.info('******Finish {0}!******'.format(trans_obj))
