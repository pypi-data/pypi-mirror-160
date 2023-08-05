import re

from markdown.preprocessors import Preprocessor



class TreeDotPreprocessor(Preprocessor):
    """
    🏠 
    """
    # TODO: Add a include pattern that matches well.

    def run(self, lines):
        for index, line in enumerate(lines):
            g = re.match("^\$pydantic: (.*)$", l)
            if g:
                cls_name = g.group(1)
                structs = analyze(cls_name)
                if structs is None:
                    print(
                        f"warning: mdantic pattern detected but failed to import module: {cls_name}"
                    )
                    continue
                tabs = fmt_tab(structs)
                table_str = ""
                for cls, tab in tabs.items():
                    table_str += "\n" + f"=={cls}==" + "\n\n" + str(tab) + "\n"
                lines = lines[:i] + [table_str] + lines[i + 1 :]

        return lines
