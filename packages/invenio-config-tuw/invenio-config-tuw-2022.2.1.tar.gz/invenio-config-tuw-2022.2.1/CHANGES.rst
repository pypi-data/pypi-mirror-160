..
    Copyright (C) 2020 - 2021 TU Wien.

    Invenio-Config-TUW is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version 2021.1 (released 2021-07-15)

- Initial public release.
- Update the list of citation styles


Version 2021.2 (released 2021-12-07, updated 2021-12-20)

- Make ready for InvenioRDM v7
- Add requests permission policy
- Enforce a rate limit for HTTP requests
- Change method of overriding the record permission policy
- Add datacite and oai_datacite metadataPrefixes to the OAI endpoint


Version 2022.1 (released 2022-03-23, updated 2022-04-06)

- Update permissions for creating and editing drafts
- Use the OAI metadata implementation from Invenio-RDM-Records
- Change the default file size and bucket quota limits to 75GB


Version 2022.2 (released 2022-07-19, updated 2022-07-20)

- v9 compat: Chase changes in Invenio-{Accounts,OAuthClient} 2.x
- v9 compat: Update permission policies
- v9 compat: Hack in permission policy for communities
- Refactor permissions and config
- Remove leftover views.py
- Set deposit form file size limits
- Fix permissions
