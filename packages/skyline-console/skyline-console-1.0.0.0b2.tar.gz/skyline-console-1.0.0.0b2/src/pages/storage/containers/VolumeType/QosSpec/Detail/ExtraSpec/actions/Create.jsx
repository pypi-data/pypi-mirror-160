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
import { ModalAction } from 'containers/Action';
import globalQosSpecKeyStore from 'stores/cinder/qos-spec-key';

export class Create extends ModalAction {
  static id = 'create';

  static title = t('Create Extra Specs');

  get name() {
    return t('Create Extra Specs');
  }

  static policy = 'volume_extension:qos_specs_manage:update';

  static allowed = () => Promise.resolve(true);

  get instanceName() {
    return this.values.keyname;
  }

  get keysMap() {
    return [
      { label: 'read_iops_sec', value: 'read_iops_sec' },
      { label: 'read_iops_sec_per_gb', value: 'read_iops_sec_per_gb' },
      { label: 'read_iops_sec_per_gb_min', value: 'read_iops_sec_per_gb_min' },
      { label: 'read_iops_sec_max', value: 'read_iops_sec_max' },
      { label: 'write_iops_sec', value: 'write_iops_sec' },
      { label: 'write_iops_sec_per_gb', value: 'write_iops_sec_per_gb' },
      {
        label: 'write_iops_sec_per_gb_min',
        value: 'write_iops_sec_per_gb_min',
      },
      { label: 'write_iops_sec_max', value: 'write_iops_sec_max' },
      { label: 'total_iops_sec', value: 'total_iops_sec' },
      { label: 'total_iops_sec_per_gb', value: 'total_iops_sec_per_gb' },
      {
        label: 'total_iops_sec_per_gb_min',
        value: 'total_iops_sec_per_gb_min',
      },
      { label: 'total_iops_sec_max', value: 'total_iops_sec_max' },
      { label: 'read_bytes_sec', value: 'read_bytes_sec' },
      { label: 'read_bytes_sec_per_gb', value: 'read_bytes_sec_per_gb' },
      {
        label: 'read_bytes_sec_per_gb_min',
        value: 'read_bytes_sec_per_gb_min',
      },
      { label: 'read_bytes_sec_max', value: 'read_bytes_sec_max' },
      { label: 'write_bytes_sec', value: 'write_bytes_sec' },
      { label: 'write_bytes_sec_per_gb', value: 'write_bytes_sec_per_gb' },
      {
        label: 'write_bytes_sec_per_gb_min',
        value: 'write_bytes_sec_per_gb_min',
      },
      { label: 'write_bytes_sec_max', value: 'write_bytes_sec_max' },
      { label: 'total_bytes_sec', value: 'total_bytes_sec' },
      { label: 'total_bytes_sec_per_gb', value: 'total_bytes_sec_per_gb' },
      {
        label: 'total_bytes_sec_per_gb_min',
        value: 'total_bytes_sec_per_gb_min',
      },
      { label: 'total_bytes_sec_max', value: 'total_bytes_sec_max' },
    ];
  }

  get defaultValue() {
    const value = {
      keyname: this.keysMap[0].value,
    };
    return value;
  }

  get formItems() {
    return [
      {
        name: 'keyname',
        label: t('Key'),
        type: 'select',
        options: this.keysMap,
        placeholder: t('Please select key'),
      },
      {
        name: 'value',
        label: t('Value'),
        type: 'input',
        placeholder: t('Please input value'),
        required: true,
      },
    ];
  }

  init() {
    this.store = globalQosSpecKeyStore;
  }

  onSubmit = (values) => {
    const { id } = this.containerProps.detail;
    const { keyname, value } = values;
    const qos_specs = { [keyname]: value };
    return this.store.createOrUpdate(id, qos_specs);
  };
}

export default inject('rootStore')(observer(Create));
