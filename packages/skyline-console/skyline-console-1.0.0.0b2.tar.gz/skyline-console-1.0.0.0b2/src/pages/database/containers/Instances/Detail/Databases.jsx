// Copyright 2021 99cloud
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import Base from 'containers/List';
import { inject, observer } from 'mobx-react';
import { InstancesDatabasesStore } from 'stores/trove/instances-database';
import actions from './DatabaseAction';

export class Databases extends Base {
  init() {
    this.store = new InstancesDatabasesStore();
  }

  get rowKey() {
    return 'name';
  }

  get name() {
    return 'Databases';
  }

  get policy() {
    return 'instance:detail';
  }

  get aliasPolicy() {
    return 'trove:instance:detail';
  }

  get actionConfigs() {
    if (this.isAdminPage) {
      return actions.actionConfigsAdmin;
    }
    return actions.actionConfigs;
  }

  get hideCustom() {
    return true;
  }

  getColumns = () => {
    return [
      {
        title: t('Database Name'),
        dataIndex: 'name',
      },
    ];
  };
}

export default inject('rootStore')(observer(Databases));
