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

import { inject, observer } from 'mobx-react';
import globalImageStore from 'stores/glance/image';
import { ModalAction } from 'containers/Action';
import KeyValueInput from 'components/FormItem/KeyValueInput';
import { MetadataStore } from 'stores/glance/metadata';
import { isEmpty, has } from 'lodash';
import { isOwner } from 'resources/glance/image';

export class ManageMetadata extends ModalAction {
  static id = 'ManageMetadata';

  static title = t('Manage Metadata');

  init() {
    this.store = globalImageStore;
    this.metadataStore = new MetadataStore();
    this.getMetadata();
  }

  get name() {
    return t('Manage Metadata');
  }

  static get modalSize() {
    return 'large';
  }

  getModalSize() {
    return 'large';
  }

  get wrapperCol() {
    return {
      xs: { span: 18 },
      sm: { span: 20 },
    };
  }

  static policy = 'modify_image';

  static allowed = (item, containerProps) => {
    const { isAdminPage } = containerProps;
    return Promise.resolve(isOwner(item) || isAdminPage);
  };

  async getMetadata() {
    const resourceType = 'OS::Glance::Image';
    await this.metadataStore.fetchList({
      manage: true,
      resource_types: resourceType,
    });
    this.updateDefaultValue();
  }

  get metadata() {
    return this.metadataStore.list.data || [];
  }

  getItemMetadata() {
    const {
      container_format,
      disk_format,
      id,
      min_disk,
      min_ram,
      name,
      protected: imageProtected,
      tags,
      visibility,
      owner,
      created_at,
      is_public,
      updated_at,
      status,
      locations,
      file,
      size,
      image_type,
      self,
      virtual_size,
      ...rest
    } = this.item.originData;
    return rest;
  }

  checkKeyInSystem = (key) => {
    const item = this.metadata.find((it) => {
      const { detail: { properties = {} } = {} } = it;
      return Object.keys(properties).indexOf(key) >= 0;
    });
    return !!item;
  };

  parseExistMetadata() {
    const customs = [];
    const systems = {};
    if (this.metadata.length > 0) {
      const metadata = this.getItemMetadata();
      Object.keys(metadata).forEach((key) => {
        if (this.checkKeyInSystem(key)) {
          systems[key] = metadata[key];
        } else {
          customs.push({
            index: customs.length,
            value: { key, value: metadata[key] },
          });
        }
      });
    }
    return {
      customs,
      systems,
    };
  }

  get defaultValue() {
    const { name } = this.item;
    const { customs, systems } = this.parseExistMetadata();
    const value = {
      name,
      customs,
      systems,
    };
    return value;
  }

  checkCustoms = (values) => {
    if (isEmpty(values)) {
      return true;
    }
    const item = values.find((it) => {
      const { key, value } = it.value || {};
      return !key || value === undefined || value === null;
    });
    return !item;
  };

  hasNoValue = (values) => {
    const item = Object.keys(values).find((it) => values[it] === undefined);
    return !!item;
  };

  get formItems() {
    return [
      {
        name: 'name',
        label: t('Name'),
        type: 'label',
        iconType: 'aggregate',
      },
      {
        name: 'customs',
        label: t('Custom Metadata'),
        type: 'add-select',
        itemComponent: KeyValueInput,
        addText: t('Add Custom Metadata'),
        validator: (rule, value) => {
          if (!this.checkCustoms(value)) {
            // eslint-disable-next-line prefer-promise-reject-errors
            return Promise.reject(t('Please enter complete key value!'));
          }
          return Promise.resolve();
        },
      },
      {
        name: 'systems',
        label: t('Metadata'),
        type: 'metadata-transfer',
        metadata: this.metadata,
        validator: (rule, value) => {
          if (this.hasNoValue(value)) {
            // eslint-disable-next-line prefer-promise-reject-errors
            return Promise.reject(t('Please input value'));
          }
          return Promise.resolve();
        },
      },
    ];
  }

  onSubmit = (values) => {
    const { customs: oldCustoms, systems: oldSystems } =
      this.parseExistMetadata();
    const { customs, systems } = values;
    const adds = [];
    const removes = [];
    const replaces = [];
    customs.forEach((it) => {
      const { key, value } = it.value || {};
      const oldItem = oldCustoms.find((c) => c.value.key === key);
      if (!oldItem) {
        adds.push(it.value);
      } else if (oldItem.value.value !== value) {
        replaces.push(it.value);
      }
    });
    Object.keys(systems).forEach((key) => {
      const item = {
        key,
        value: systems[key],
      };
      if (!has(oldSystems, key)) {
        adds.push(item);
      } else if (systems[key] !== oldSystems[key]) {
        replaces.push(item);
      }
    });
    oldCustoms.forEach((it) => {
      const item = customs.find((custom) => custom.value.key === it.value.key);
      if (!item) {
        removes.push(it.value.key);
      }
    });
    Object.keys(oldSystems).forEach((key) => {
      if (!has(systems, key)) {
        removes.push(key);
      }
    });
    const changeValues = [];
    adds.forEach((it) => {
      changeValues.push({
        op: 'add',
        path: `/${it.key}`,
        value: it.value,
      });
    });
    replaces.forEach((it) => {
      changeValues.push({
        op: 'replace',
        path: `/${it.key}`,
        value: it.value,
      });
    });
    removes.forEach((it) => {
      changeValues.push({
        op: 'remove',
        path: `/${it}`,
      });
    });
    if (changeValues.length === 0) {
      return Promise.resolve();
    }
    return this.store.update({ id: this.item.id }, changeValues);
  };
}

export default inject('rootStore')(observer(ManageMetadata));
