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

import { observer, inject } from 'mobx-react';
import Base from 'containers/TabList';
import NetworkTab from './Network';

export class Network extends Base {
  get tabs() {
    const tabs = [
      {
        title: t('Current Project Network'),
        key: 'projectNetwork',
        component: NetworkTab,
      },
      {
        title: t('Shared Network'),
        key: 'sharedNetwork',
        component: NetworkTab,
      },
      {
        title: t('External Network'),
        key: 'externalNetwork',
        component: NetworkTab,
      },
    ];
    if (this.hasAdminRole) {
      tabs.push({
        title: t('All Network'),
        key: 'allNetwork',
        component: NetworkTab,
      });
    }
    return tabs;
  }
}

export default inject('rootStore')(observer(Network));
