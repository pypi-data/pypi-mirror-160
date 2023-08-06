import enum
import time
from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property

from ..utils.kabaret.flow_entities.entities import EntityView

from .file import FileSystemMap
from .maputils import SimpleCreateAction
from .task_manager import CreateTaskDefaultFiles, ManageTasksAction


class IconSize(enum.Enum):

    SMALL  = 0
    MEDIUM = 1
    LARGE  = 2


class Task(Entity):
    """
    Defines an arbitrary task containing a list of files.

    Instances provide the `task` and `task_display_name` keys
    in their contextual dictionary (`settings` context).
    """
    
    display_name = Property().ui(hidden=True)
    enabled      = Property().ui(hidden=True, editor='bool')
    icon_small   = Property().ui(hidden=True)
    icon_medium  = Property().ui(hidden=True)
    icon_large   = Property().ui(hidden=True)

    files = flow.Child(FileSystemMap).ui(
        expanded=True,
        action_submenus=True,
        items_action_submenus=True
    )

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]} · {split[9]}'
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                task=self.name(),
                task_display_name=self.display_name.get(),
            )
    
    def get_icon(self, size=IconSize.SMALL):
        if size == IconSize.SMALL:
            return self.icon_small.get()
        elif size == IconSize.MEDIUM:
            return self.icon_medium.get()
        else:
            return self.icon_large.get()


class TaskCollection(EntityView):
    """
    Defines a collection of tasks.
    """

    add_task = flow.Child(SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Task)
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.get_task_collection().collection_name()


# Managed tasks
# -------------------------


class ManagedTask(Task):
    """
    A ManagedTask provides features handled by the task
    manager of the project.
    """

    create_dft_files = flow.Child(CreateTaskDefaultFiles).ui(
        label='Create default files'
    )


class ManagedTaskCollection(TaskCollection):

    manage_tasks = flow.Child(ManageTasksAction).ui(
        label='Manage tasks'
    )

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(ManagedTask)
    
    def mapped_names(self, page_num=0, page_size=None):
        names = super(ManagedTaskCollection, self).mapped_names(
            page_num, page_size
        )
        # Sort tasks by their positions configured in the project's default tasks
        mgr = self.root().project().get_task_manager()
        names = sorted(
            names,
            key=lambda n: mgr.default_tasks[n].position.get()
        )
        return names
    
    def _fill_row_cells(self, row, item):
        mgr = self.root().project().get_task_manager()
        row['Name'] = mgr.get_task_display_name(item.name())

    def _fill_row_style(self, style, item, row):
        mgr = self.root().project().get_task_manager()
        style['icon'] = mgr.get_task_icon(item.name())
        style['foreground-color'] = mgr.get_task_color(item.name())
