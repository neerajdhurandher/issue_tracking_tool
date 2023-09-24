# Issue Tracking Tool

## Overview

The Issue Tracking Tool is a Django application designed to manage and track issues within projects. It provides features similar to JIRA, allowing users to create projects, sprints, issues, comments, watchers, and labels. The application includes two main apps: User and Project.

## User App

The User app includes all user-related functionalities such as registration, login, authentication, and user profile management. The app contains the following files and folders:

1. `models.py`: Contains the User model for storing user information.
2. `views.py`: Includes views for user registration, login, authentication, and profile management.
3. `urls.py`: Defines the URLs for user-related functionalities.
4. `serializers.py`: Serializers for user registration and profile information.
5. `utils.py`: Utility functions for user-related operations.

## Project App

The Project app is responsible for managing all project-related functionalities. It includes the following folders and files:

### Project Folder

1. `views_project.py`: Views for creating, updating, and deleting projects.
2. `serializers_project.py`: Serializers for project information.

### Sprint Folder

1. `views_sprint.py`: Views for managing sprints within a project.
2. `serializers_sprint.py`: Serializers for sprint information.

### Issue Folder

1. `views_issue.py`: Views for creating, updating, and deleting issues within a project.
2. `serializers_issue.py`: Serializers for issue information.

### Watcher Folder

1. `views_watcher.py`: Views for managing watchers of projects and issues.
2. `serializers_watcher.py`: Serializers for watcher information.

### Comment Folder

1. `views_comment.py`: Views for creating, updating, and deleting comments on issues.
2. `serializers_comment.py`: Serializers for comment information.

### Label Folder

1. `views_label.py`: Views for managing labels within a project.
2. `serializers_label.py`: Serializers for label information.

#### model.py

* `BaseModel`
* `ProjectModel`
* `UserProjectRelationModel`
* `SprintModel`
* `IssueModel`
* `WatcherModel`
* `CommentModel`
* `LabelModel`

`utils.py`: Contains utility functions used by the project app.

`constant.py`: Contains constant values used by the project app.

## Django Default Files and Folders

In addition to the above files and folders specific to the application, Django includes default files and folders that are required for the application's functionality. Some of the important default files and folders are:

1. `manage.py`: The command-line utility for managing Django projects.
2. `admin.py`: Contains admin configurations for the Django application.
3. `settings.py`: Configuration settings for the Django application.
4. `urls.py`: Contains the primary URL routing configuration for the project.
5. `migrations/`: Stores database migrations to manage schema changes over time.

## Conclusion

The Issue Tracking Tool is a comprehensive Django application that provides all necessary functionalities for managing projects
