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
import Base from 'containers/List';
import {
  volumeTransitionStatuses,
  volumeFilters,
  getVolumeColumnsList,
} from 'resources/cinder/volume';
import globalVolumeStore, { VolumeStore } from 'stores/cinder/volume';
import { InstanceVolumeStore } from 'stores/nova/instance-volume';
import { emptyActionConfig } from 'utils/constants';
import actionConfigs from './actions';

export class Volume extends Base {
  init() {
    if (this.inDetailPage) {
      this.store = new InstanceVolumeStore();
      this.downloadStore = this.store;
    } else {
      this.store = globalVolumeStore;
      this.downloadStore = new VolumeStore();
    }
  }

  get policy() {
    return 'volume:get_all';
  }

  get name() {
    return t('volumes');
  }

  get isRecycleBinDetail() {
    return this.inDetailPage && this.path.includes('recycle-bin');
  }

  get actionConfigs() {
    if (this.isRecycleBinDetail) {
      return emptyActionConfig;
    }
    if (this.isAdminPage) {
      return this.inDetailPage
        ? actionConfigs.instanceDetailAdminConfig
        : actionConfigs.adminConfig;
    }
    return this.inDetailPage
      ? actionConfigs.instanceDetailConfig
      : actionConfigs.actionConfigs;
  }

  get transitionStatusList() {
    return volumeTransitionStatuses;
  }

  get isFilterByBackend() {
    return !this.inDetailPage;
  }

  get isSortByBackend() {
    return this.isFilterByBackend;
  }

  get adminPageHasProjectFilter() {
    return true;
  }

  get defaultSortKey() {
    return 'created_at';
  }

  getColumns = () => {
    return getVolumeColumnsList(this);
  };

  get searchFilters() {
    return volumeFilters;
  }

  updateFetchParams = (params) => {
    if (this.inDetailPage) {
      const { match, detail } = this.props;
      const { id } = match.params;
      const { tenant_id: projectId, name } = detail || {};
      return {
        ...params,
        serverId: id,
        serverName: name,
        projectId,
      };
    }
    return params;
  };
}

export default inject('rootStore')(observer(Volume));
