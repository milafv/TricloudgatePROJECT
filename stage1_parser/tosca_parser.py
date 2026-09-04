# tosca_parser.py
# Milaf Alajlan
# Component: TOSCA Parser


import yaml
import os


class TOSCAParser:
    """
    يقرأ ملفات TOSCA 2.0 بصيغة YAML
    ولسه اشتغل على إضافة التحقق الكامل للملف
    """

    def __init__(self):
        # نخزن هنا رسائل الايرور
        self.errors = []
        # TODO: نضيف ليست للتحذيرات بعدين

    def parse(self, file_path):
        """
        يقرأ ملف TOSCA بصيغة YAML ويرجع محتواه.
        ولسه احتاج اضيف عليه فحوصات تحقق أكثر.
        """

        self.errors = []

        print(f"[TOSCAParser] Reading file: {file_path}")

        #  هل الملف موجود؟
        if not os.path.exists(file_path):
            self._add_error(f"File not found: '{file_path}'")
            return None

        #  هل الملف بصيغة YAML؟
        if not file_path.endswith('.yaml') and not file_path.endswith('.yml'):
            self._add_error(f"Wrong file type — must be .yaml or .yml")
            return None

        # TODO: اضيف تحقق من حجم الملف بعدين

        # نحاول نقرأ الملف
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self._add_error(f"Could not read file: {str(e)}")
            return None

        #  هل الملف فيه محتوى؟
        if content is None:
            self._add_error("File is empty")
            return None

        # اتأكد إن الملف فيه قسم node_templates
        if 'node_templates' not in content:
            self._add_error("File has no node_templates section")
            return None

        # TODO: نتحقق إن كل عقدة فيها الحقول المطلوبة
        # TODO: نتأكد إن إصدار توسكا متوافق
       
        node_count = len(content['node_templates'])
        print(f"[TOSCAParser] Found {node_count} node(s) — basic validation passed")
        print(f"[TOSCAParser] Note: full validation not implemented yet")

        return content

    def _add_error(self, message):
        self.errors.append(message)
        print(f"[TOSCAParser] ERROR: {message}")

    def get_errors(self):
        return self.errors

    # TODO: نضيف دالة تتحقق من العلاقات بين العقد
    # TODO: نضيف دالة تتأكد من أنواع خصائص العقد

