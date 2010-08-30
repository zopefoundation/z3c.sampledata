from z3c.sampledata import _
from z3c.sampledata.interfaces import ISampleManager
from zope import component
from zope import interface
from zope import schema
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL
import zope.formlib.form
import zope.app.pagetemplate.namedtemplate
import zope.formlib.interfaces


class Managers(object):

    template = ViewPageTemplateFile("managers.pt")

    def managers(self):
        m = [name for name, util in component.getUtilitiesFor(ISampleManager)]
        return m

    def __call__(self):
        self.update()
        return self.template()

    def update(self):
        if 'manager' in self.request:
            managerName = self.request['manager']
            self.request.response.redirect(
                absoluteURL(self.context, self.request)+
                '/@@generatesample.html?manager="%s"'%(managerName))


class IGenerateSchema(interface.Interface):
    """Schema for the minimal generator parameters"""

    seed = schema.TextLine(
            title = _(u'Seed'),
            description =  _(u'A seed for the random generator'),
            default = u'sample',
            required=False,
            )


class Generate(zope.formlib.form.EditForm):
    """Edit all generator parameters for a given manager"""

    base_template = zope.formlib.form.EditForm.template
    template = ViewPageTemplateFile('generate.pt')

    workDone = False

    def setUpWidgets(self, ignore_request=False):
        managerName = self.request['manager']
        manager = component.getUtility(ISampleManager, name=managerName)
        plugins = manager.orderedPlugins()
        self.form_fields = zope.formlib.form.Fields()
        self.subforms = []
        subform = Generator(context=self.context,
                            request=self.request,
                            schema=IGenerateSchema,
                            prefix='generator')
        subform.form_fields = zope.formlib.form.Fields(IGenerateSchema)
        self.subforms.append(subform)
        for plugin in plugins:
            if plugin.generator.schema is None:
                continue
            subform = Generator(context=self.context,
                                request=self.request,
                                plugin=plugin.generator,
                                prefix=plugin.name)
            subform.form_fields = zope.formlib.form.Fields(
                plugin.generator.schema)
            self.subforms.append(subform)
        super(Generate, self).setUpWidgets(ignore_request=ignore_request)

    @zope.formlib.form.action(_("Generate"))
    def handle_generate_action(self, action, data):
        managerName = self.request['manager']
        manager = component.getUtility(ISampleManager, name=managerName)
        generatorData = {}
        for subform in self.subforms:
            subform.update()
            formData = {}
            errors = zope.formlib.form.getWidgetsData(
                subform.widgets, subform.prefix, formData)
            generatorData[subform.prefix] = formData
        gen = generatorData.get('generator', {})
        seed = gen.get('seed', None)
        self.workedOn = manager.generate(context=self.context,
                                         param=generatorData,
                                         seed=seed)
        self.workDone = True
        self.actions = []

    def manager(self):
        return self.request['manager']


class Generator(zope.formlib.form.AddForm):
    """An editor for a single generator"""
    interface.implements(zope.formlib.interfaces.ISubPageForm)

    template = zope.app.pagetemplate.namedtemplate.NamedTemplate('default')

    actions = []

    def __init__(self, context, request, plugin=None, schema=None, prefix=''):
        self.plugin = plugin
        self.schema = schema
        self.prefix = prefix
        super(Generator, self).__init__(context, request)
