# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader

class ImportPlugin(BaseAdminPlugin):
    """
    导入插件
    """
    import_excel = False

    # 插件的入口函数，当返回True时，加载该插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)
    
    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.imports.html'))

site.register_plugin(ImportPlugin, ListAdminView)
