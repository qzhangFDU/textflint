r"""
SM Generator Class
============================================

"""
__all__ = ['SMGenerator']

from .generator import Generator


class SMGenerator(Generator):
    r"""
    SM Generator aims to apply SM data generation function.

    """
    def __init__(
        self,
        task='SM',
        max_trans=1,
        fields=['sentence1', 'sentence2'],
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

    def _check_fields(self):
        r"""
        Check whether fields are legal.

        :return:
        """
        if isinstance(self.fields, str):
            self.fields = [self.fields]
        elif isinstance(self.fields, list):
            pass
        else:
            raise ValueError(
                f'Task {self.task} not support input fields'
                f' type: {type(self.fields)}'
            )

        for field in self.fields:
            if field not in ['sentence1', 'sentence2', 'y']:
                raise ValueError(
                    f'Task {self.task} not support input fields: {field}'
                )

