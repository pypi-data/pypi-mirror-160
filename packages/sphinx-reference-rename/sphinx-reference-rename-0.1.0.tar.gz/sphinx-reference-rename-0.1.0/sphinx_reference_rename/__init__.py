from typing import Any
from typing import Dict
from typing import Optional

from docutils.nodes import Element
from docutils.nodes import TextElement

import sphinx
from sphinx.addnodes import pending_xref
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment


def missing_reference(app: Sphinx, env: BuildEnvironment, node: pending_xref,
                      contnode: TextElement) -> Optional[Element]:
    newtarget = app.config.sphinx_reference_rename_mapping.get(node["reftarget"])
    if newtarget is not None:
        node["reftarget"] = newtarget


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value('sphinx_reference_rename_mapping', {}, True)
    app.connect('missing-reference', missing_reference, priority=400)
    return {
        'version': sphinx.__display_version__,
        'env_version': 1,
        'parallel_read_safe': True
    }
