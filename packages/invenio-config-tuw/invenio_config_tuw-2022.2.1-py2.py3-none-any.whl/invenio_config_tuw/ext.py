# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing some customizations and configuration for TU Wien."""

from functools import partial

from flask_security.signals import user_registered

from . import config
from .auth.utils import auto_trust_user
from .permissions import TUWCommunitiesPermissionPolicy


@user_registered.connect
def auto_trust_new_user(sender, user, **kwargs):
    # NOTE: 'sender' and 'kwargs' are ignored, but they're required to match the
    #       expected function signature
    # NOTE: this function won't be called when a user is created via the CLI
    #       ('invenio users create'), because it doesn't send the 'user_registered'
    #       signal
    auto_trust_user(user)


class InvenioConfigTUW(object):
    """Invenio-Config-TUW extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self._overrides = set()
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-config-tuw"] = self
        self.override_communities_permissions(app)

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            if len(k.replace("_", "")) >= 3 and k.isupper():
                app.config.setdefault(k, getattr(config, k))

        # the datacenter symbol seems to be the username for DataCite Fabrica
        if app.config.get("DATACITE_ENABLED", False):
            key = "DATACITE_DATACENTER_SYMBOL"
            if not app.config.get(key, None):
                app.config[key] = app.config["DATACITE_USERNAME"]

    def override_communities_permissions(self, app):
        """Override permission policy class for communities."""
        # TODO change this as soon as Invenio-Communities allows to do it via config
        key = "invenio-communities"
        if key in self._overrides:
            return

        communities = app.extensions.get(key, None)
        if communities is not None and communities.service is not None:
            # override the permission policy class for all communities services
            svc = communities.service
            svc.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
            svc.files.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
            svc.members.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
            self._overrides.add(key)
            app.logger.debug("Communities permissions overridden.")
        else:
            # if the override failed, schedule it before the first request
            app.logger.warning(
                "Could not override communities permissions: extension not loaded!"
            )
            override_func = partial(self.override_communities_permissions, app)
            app.before_first_request_funcs.append(override_func)
