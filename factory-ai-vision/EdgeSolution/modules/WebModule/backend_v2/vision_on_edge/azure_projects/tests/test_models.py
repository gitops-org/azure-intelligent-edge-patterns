"""App model tests.
"""

from unittest import mock

import pytest

from ..exceptions import ProjectCustomVisionError, ProjectWithoutSettingError
from .conftest import MockedProject
from .factories import ProjectFactory

pytestmark = pytest.mark.django_db


def test_create_1():
    """test_create_1.

    Type:
        Negative

    Description:
        Create projet given invalid/null azure_setting
    """
    project = ProjectFactory()
    project.customvision_id = "valid_project_id"
    project.name = "wrong project name"
    project.save()
    assert project.customvision_id == "valid_project_id"
    assert project.name == MockedProject().name


@mock.patch(
    "vision_on_edge.azure_projects.models.Project.get_project_obj",
    mock.MagicMock(side_effect=ProjectCustomVisionError),
)
def test_create_2():
    """test_create_1.

    Type:
        Negative

    Description:
        Create projet given invalid customvision_id
    """
    project = ProjectFactory()
    project.customvision_id = "super_valid_project_id"
    project.name = "Random"
    project.save()
    assert project.customvision_id == ""
    assert project.name == "Random"


@mock.patch(
    "vision_on_edge.azure_projects.models.Project.get_project_obj",
    mock.MagicMock(side_effect=ProjectWithoutSettingError),
)
def test_create_project_with_null_setting():
    """test_create_1.

    Type:
        Negative

    Description:
        Create project with null setting
    """
    project = ProjectFactory()
    project.customvision_id = "super_valid_project_id"
    project.name = "Random"
    project.setting = None
    project.save()
    assert project.customvision_id == ""
    assert project.name == "Random"


def test_update_invalid_customvision_id():
    """test_update_invalid_customvision_id.

    If project from valid id to invalid id. customvision_id set to ""
    """
    project = ProjectFactory()
    project.customvision_id = "super_valid_project_id"
    project.name = "Random"
    project.save()
    assert project.customvision_id == "super_valid_project_id"
    assert project.name == MockedProject().name

    with mock.patch(
        "vision_on_edge.azure_projects.models.Project.get_project_obj",
        mock.MagicMock(side_effect=ProjectCustomVisionError),
    ):
        project.customvision_id = "invalid_project_id"
        project.name = "Random2"
        project.save()
    assert project.customvision_id == ""
    assert project.name == "Random2"


def test_update_valid_customvision_id():
    """test_create_1.

    If project from valid id to invalid id. customvision_id set to ""
    """
    with mock.patch(
        "vision_on_edge.azure_projects.models.Project.get_project_obj",
        mock.MagicMock(side_effect=ProjectWithoutSettingError),
    ):
        project = ProjectFactory()
        project.customvision_id = "super_valid_project_id"
        project.name = "Random"
        project.save()
        assert project.customvision_id == ""
        assert project.name == "Random"

    project.customvision_id = "new_project_id"
    project.name = "Name that should be replaced"
    project.save()
    assert project.customvision_id == "new_project_id"
    assert project.name == MockedProject().name


@pytest.mark.fast
def test_get_project():
    project = ProjectFactory()
    assert project.get_project_obj().name == MockedProject().name
