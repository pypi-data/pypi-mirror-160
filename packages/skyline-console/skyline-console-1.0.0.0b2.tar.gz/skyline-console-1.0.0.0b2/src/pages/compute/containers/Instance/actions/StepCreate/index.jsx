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

import React from 'react';
import { inject, observer } from 'mobx-react';
import { toJS } from 'mobx';
import { InputNumber, Badge, message as $message } from 'antd';
import { StepAction } from 'containers/Action';
import globalServerStore from 'stores/nova/instance';
import globalProjectStore from 'stores/keystone/project';
import classnames from 'classnames';
import { isEmpty, isFinite, isString } from 'lodash';
import { getUserData } from 'resources/nova/instance';
import { getGiBValue } from 'utils/index';
import Notify from 'components/Notify';
import ConfirmStep from './ConfirmStep';
import SystemStep from './SystemStep';
import NetworkStep from './NetworkStep';
import BaseStep from './BaseStep';
import styles from './index.less';

export class StepCreate extends StepAction {
  static id = 'instance-create';

  static title = t('Create Instance');

  static path = (_, containerProps) => {
    const { detail, match } = containerProps || {};
    if (!detail || isEmpty(detail)) {
      return '/compute/instance/create';
    }
    if (match.path.indexOf('/compute/server') >= 0) {
      return `/compute/instance/create?servergroup=${detail.id}`;
    }
  };

  init() {
    this.store = globalServerStore;
    this.projectStore = globalProjectStore;
    this.getQuota();
    this.status = 'success';
    this.errorMsg = '';
  }

  static policy = [
    'os_compute_api:servers:create',
    'os_compute_api:os-availability-zone:list',
  ];

  static allowed(_, containerProps) {
    const { isAdminPage = false } = containerProps;
    return Promise.resolve(!isAdminPage);
  }

  async getQuota() {
    await Promise.all([
      this.projectStore.fetchProjectNovaQuota(),
      this.projectStore.fetchProjectCinderQuota(),
    ]);
    this.onCountChange(1);
  }

  get disableNext() {
    return !!this.errorMsg;
  }

  get disableSubmit() {
    return !!this.errorMsg;
  }

  get instanceQuota() {
    const { instances: { left = 0 } = {} } =
      toJS(this.projectStore.novaQuota) || {};
    if (left === -1) {
      return Infinity;
    }
    return left;
  }

  get name() {
    return t('Create instance');
  }

  get enableCinder() {
    return this.props.rootStore.checkEndpoint('cinder');
  }

  get listUrl() {
    const { image, volume, servergroup } = this.locationParams;
    if (image) {
      return this.getRoutePath('image');
    }
    if (volume) {
      return this.getRoutePath('volume');
    }
    if (servergroup) {
      return this.getRoutePath('serverGroupDetail', { id: servergroup });
    }
    return this.getRoutePath('instance');
  }

  get hasConfirmStep() {
    return false;
  }

  get steps() {
    return [
      {
        title: t('Base Config'),
        component: BaseStep,
      },
      {
        title: t('Network Config'),
        component: NetworkStep,
      },
      {
        title: t('System Config'),
        component: SystemStep,
      },
      {
        title: t('Confirm Config'),
        component: ConfirmStep,
      },
    ];
  }

  get instanceName() {
    const { name, count = 1 } = this.values || {};
    if (count === 1) {
      return this.unescape(name);
    }
    return this.unescape(
      new Array(count)
        .fill(count)
        .map((_, index) => `${name}-${index + 1}`)
        .join(', ')
    );
  }

  get successText() {
    return t(
      'The creation instruction was issued successfully, instance: {name}. \n You can wait for a few seconds to follow the changes of the list data or manually refresh the data to get the final display result.',
      { action: this.name.toLowerCase(), name: this.instanceName }
    );
  }

  get showQuota() {
    return true;
  }

  get quotaInfo() {
    const {
      instances = {},
      cores = {},
      ram = {},
    } = toJS(this.projectStore.novaQuota) || {};
    const { limit } = instances || {};
    if (!limit) {
      return [];
    }
    const { data = {} } = this.state;
    const { count = 1 } = data;
    const instanceQuotaInfo = {
      ...instances,
      add: count,
      name: 'instance',
      title: t('Instance'),
      // type: 'line',
    };

    const { newCPU, newRam } = this.getFlavorInput();
    const cpuQuotaInfo = {
      ...cores,
      add: newCPU,
      name: 'cpu',
      title: t('CPU'),
      type: 'line',
    };

    const ramQuotaInfo = {
      ...ram,
      add: newRam,
      name: 'ram',
      title: t('Memory (GiB)'),
      type: 'line',
    };

    const volumeQuota = this.getVolumeQuota();
    const { totalNewCount, totalNewSize } = this.getVolumeInputMap();
    const volumeQuotaInfo = {
      ...volumeQuota.volumes,
      add: totalNewCount,
      name: 'volume',
      title: t('Volume'),
      type: 'line',
    };
    const volumeSizeQuotaInfo = {
      ...volumeQuota.gigabytes,
      add: totalNewSize,
      name: 'volumeSize',
      title: t('Volume Size'),
      type: 'line',
    };
    return [
      instanceQuotaInfo,
      cpuQuotaInfo,
      ramQuotaInfo,
      volumeQuotaInfo,
      volumeSizeQuotaInfo,
    ];
  }

  get errorText() {
    const { status } = this.state;
    if (status === 'error') {
      return t(
        'Unable to create instance: insufficient quota to create resources.'
      );
    }
    if (this.ipBatchError) {
      return t(
        'Unable to create instance: batch creation is not supported when specifying IP.'
      );
    }
    return t(
      'The creation instruction has been issued, please refresh to see the actual situation in the list.'
    );
  }

  onCountChange = (value) => {
    const { data } = this.state;
    this.setState({
      data: {
        ...data,
        count: value,
      },
    });
  };

  getVolumeQuota() {
    const quotaAll = toJS(this.projectStore.cinderQuota) || {};
    const result = {};
    Object.keys(quotaAll).forEach((key) => {
      if (key.includes('volumes') || key.includes('gigabytes')) {
        result[key] = quotaAll[key];
      }
    });
    return result;
  }

  getQuotaMessage(value, quota, name) {
    const { left = 0 } = quota || {};
    if (left === -1) {
      return '';
    }
    if (value > left) {
      return t(
        'Insufficient {name} quota to create resources(left { quota }, input { input }).',
        { name, quota: left, input: value }
      );
    }
    return '';
  }

  getVolumeInputMap() {
    const { data } = this.state;
    const {
      systemDisk = {},
      dataDisk = [],
      count = 1,
      source: { value: sourceValue } = {},
      instanceSnapshotDisk = {},
    } = data;
    const newCountMap = {};
    const newSizeMap = {};
    let totalNewCount = 0;
    let totalNewSize = 0;
    if (sourceValue === 'instanceSnapshot' && instanceSnapshotDisk) {
      const { size, typeOption: { label } = {} } = instanceSnapshotDisk;
      if (label) {
        newCountMap[label] = !newCountMap[label] ? 1 : newCountMap[label] + 1;
        newSizeMap[label] = !newSizeMap[label]
          ? size
          : newSizeMap[label] + size;
        totalNewCount += 1 * count;
        totalNewSize += size * count;
      }
    } else if (systemDisk.type) {
      const { size } = systemDisk;
      const { label } = systemDisk.typeOption || {};
      newCountMap[label] = !newCountMap[label] ? 1 : newCountMap[label] + 1;
      newSizeMap[label] = !newSizeMap[label] ? size : newSizeMap[label] + size;
      totalNewCount += 1 * count;
      totalNewSize += size * count;
    }
    if (dataDisk) {
      dataDisk.forEach((item) => {
        if (item.value && item.value.type) {
          const { size } = item.value;
          const { label } = item.value.typeOption || {};
          newCountMap[label] = !newCountMap[label]
            ? 1 * count
            : newCountMap[label] + 1 * count;
          newSizeMap[label] = !newSizeMap[label]
            ? size * count
            : newSizeMap[label] + size * count;
          totalNewCount += 1 * count;
          totalNewSize += size * count;
        }
      });
    }
    return {
      totalNewCount,
      totalNewSize,
      newCountMap,
      newSizeMap,
    };
  }

  checkVolumeQuota() {
    if (!this.enableCinder) return '';
    let msg = '';
    const { totalNewCount, totalNewSize, newCountMap, newSizeMap } =
      this.getVolumeInputMap();
    const quotaAll = this.getVolumeQuota();
    const totalCountMsg = this.getQuotaMessage(
      totalNewCount,
      quotaAll.volumes,
      t('volume')
    );
    if (totalCountMsg) {
      return totalCountMsg;
    }
    const totalSizeMsg = this.getQuotaMessage(
      totalNewSize,
      quotaAll.gigabytes,
      t('volume gigabytes')
    );
    if (totalSizeMsg) {
      return totalSizeMsg;
    }
    Object.keys(newCountMap).forEach((key) => {
      const countMsg = this.getQuotaMessage(
        newCountMap[key],
        quotaAll[`volumes_${key}`],
        t('volume type {type}', { type: key })
      );
      if (countMsg) {
        msg = countMsg;
      }
    });
    if (msg) {
      return msg;
    }
    Object.keys(newSizeMap).forEach((key) => {
      const sizeMsg = this.getQuotaMessage(
        newSizeMap[key],
        quotaAll[`gigabytes_${key}`],
        t('volume type {type} gigabytes', { type: key })
      );
      if (sizeMsg) {
        msg = sizeMsg;
      }
    });
    return msg;
  }

  getFlavorInput() {
    const { data } = this.state;
    const { flavor = {}, count = 1 } = data;
    const { selectedRows = [] } = flavor;
    const { vcpus = 0, ram = 0 } = selectedRows[0] || {};
    const ramGiB = getGiBValue(ram);
    const newCPU = vcpus * count;
    const newRam = ramGiB * count;
    return {
      newCPU,
      newRam,
    };
  }

  checkFlavorQuota() {
    const { newCPU, newRam } = this.getFlavorInput();
    const { cores = {}, ram = {} } = this.projectStore.novaQuota;
    const { left = 0 } = cores || {};
    const { left: leftRam = 0 } = ram || {};
    if (left !== -1 && left < newCPU) {
      return this.getQuotaMessage(newCPU, cores, t('CPU'));
    }
    if (leftRam !== -1 && leftRam < newRam) {
      return this.getQuotaMessage(newRam, ram, t('Memory'));
    }
    return '';
  }

  get badgeStyle() {
    return { marginTop: 8, marginBottom: 8, marginLeft: 10, maxWidth: 600 };
  }

  renderBadge() {
    const flavorMsg = this.checkFlavorQuota();
    const volumeMsg = this.checkVolumeQuota();
    if (!flavorMsg && !volumeMsg) {
      this.status = 'success';
      this.errorMsg = '';
      return null;
    }
    this.status = 'error';
    const msg = flavorMsg || volumeMsg;
    if (this.errorMsg !== msg) {
      $message.error(msg);
    }
    this.errorMsg = msg;
    return (
      <div style={this.badgeStyle}>
        <Badge status="error" text={msg} />
      </div>
    );
  }

  renderExtra() {
    return null;
  }

  renderFooterLeft() {
    const { data } = this.state;
    const { count = 1, source: { value: sourceValue } = {} } = data;
    const configs = {
      min: 1,
      max:
        sourceValue === 'bootableVolume'
          ? 1
          : isFinite(this.instanceQuota)
          ? this.instanceQuota
          : 100,
      precision: 0,
      onChange: this.onCountChange,
      formatter: (value) => `$ ${value}`.replace(/\D/g, ''),
    };
    return (
      <div style={{ display: 'flex' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div className={styles['number-input']}>
            <span>{t('Count')}</span>
            <InputNumber
              {...configs}
              value={count}
              className={classnames(styles.input, 'instance-count')}
            />
          </div>
          {this.renderExtra()}
        </div>
        {this.renderBadge()}
      </div>
    );
  }

  getVolumeAndImageData(values) {
    if (this.status === 'error') {
      return null;
    }
    /* eslint-disable no-unused-vars */
    const {
      bootableVolume,
      dataDisk,
      image,
      instanceSnapshot,
      instanceSnapshotDisk,
      source,
      systemDisk,
    } = values;
    const { value: sourceValue } = source;
    const imageRef =
      sourceValue === 'bootableVolume'
        ? null
        : sourceValue === 'image'
        ? image.selectedRowKeys[0]
        : instanceSnapshot.selectedRowKeys[0];
    if (!this.enableCinder) {
      return {
        imageRef,
      };
    }
    let rootVolume = {};
    if (sourceValue !== 'bootableVolume') {
      const { deleteType, type, size } = systemDisk || {};
      rootVolume = {
        boot_index: 0,
        uuid: imageRef,
        source_type: 'image',
        volume_size: size,
        destination_type: 'volume',
        volume_type: type,
        delete_on_termination: deleteType === 1,
      };
      if (sourceValue === 'instanceSnapshot') {
        if (instanceSnapshotDisk) {
          delete rootVolume.volume_size;
          delete rootVolume.volume_type;
          delete rootVolume.delete_on_termination;
        }
      }
    } else {
      rootVolume = {
        boot_index: 0,
        uuid: bootableVolume.selectedRowKeys[0],
        source_type: 'volume',
        destination_type: 'volume',
      };
    }
    const dataVolumes = dataDisk
      ? dataDisk.map((it) => {
          const {
            size: volumeSize,
            type: volumeType,
            deleteType: volumeDelType,
          } = it.value || {};
          return {
            source_type: 'blank',
            volume_size: volumeSize,
            destination_type: 'volume',
            volume_type: volumeType,
            delete_on_termination: volumeDelType === 1,
          };
        })
      : [];
    if (
      sourceValue === 'image' &&
      image.selectedRows[0].disk_format === 'iso' &&
      dataVolumes[0]
    ) {
      dataVolumes[0].boot_index = 0;
      dataVolumes[0].device_type = 'disk';
      rootVolume.boot_index = 1;
      rootVolume.device_type = 'cdrom';
    }
    return {
      volumes: [rootVolume, ...dataVolumes],
      imageRef,
    };
  }

  getNetworkData(values) {
    const { networks = [], ports = {} } = values;
    let hasIp = false;
    const data = [];
    networks.forEach((it) => {
      const net = {
        uuid: it.value.network,
      };
      if (it.value.ipType === 1 && it.value.ip) {
        net.fixed_ip = it.value.ip;
        hasIp = true;
      }
      data.push(net);
    });
    const { selectedRowKeys = [] } = ports || {};
    selectedRowKeys.forEach((it) => {
      const net = {
        port: it,
      };
      data.push(net);
    });
    return {
      data,
      hasIp,
    };
  }

  getSubmitData(values) {
    if (this.status === 'error') {
      return null;
    }
    const { volumes, imageRef } = this.getVolumeAndImageData(values);
    const { data: networks, hasIp } = this.getNetworkData(values);
    const {
      availableZone,
      keypair,
      loginType,
      password,
      physicalNode,
      physicalNodeType,
      securityGroup,
      flavor,
      userData = '',
      serverGroup,
      name,
      count = 1,
    } = values;
    if (hasIp && count > 1) {
      this.ipBatchError = true;
      return null;
    }
    const { selectedRows: securityGroupSelectedRows = [] } =
      securityGroup || {};
    const server = {
      security_groups: securityGroupSelectedRows.map((it) => ({
        name: it.id,
      })),
      name,
      flavorRef: flavor.selectedRowKeys[0],
      availability_zone: availableZone.value,
      networks,
    };
    if (this.enableCinder) {
      server.block_device_mapping_v2 = volumes;
    }
    if (imageRef && !volumes) {
      server.imageRef = imageRef;
    }
    if (loginType.value === 'keypair') {
      server.key_name = keypair.selectedRowKeys[0];
    } else {
      server.adminPass = password;
    }
    if (count > 1) {
      server.min_count = count;
      server.max_count = count;
      server.return_reservation_id = true;
    }
    if (physicalNodeType.value !== 'smart') {
      server.hypervisor_hostname =
        physicalNode.selectedRows[0].hypervisor_hostname;
    }
    if (server.adminPass || userData) {
      server.user_data = btoa(getUserData(server.adminPass, userData));
    }
    const body = {
      server,
    };

    if (serverGroup && serverGroup.selectedRowKeys.length > 0) {
      body['OS-SCH-HNT:scheduler_hints'] = {
        group: serverGroup.selectedRowKeys[0],
      };
    }
    return body;
  }

  onSubmit = (body) => {
    if (!body) {
      if (this.errorMsg) {
        Notify.error(this.errorMsg);
      }
      return Promise.reject();
    }
    return this.store.create(body);
  };

  onOk = () => {
    const { data } = this.state;
    this.values = data;
    const submitData = this.getSubmitData(data);
    if (!submitData) {
      Notify.errorWithDetail(null, this.errorText);
      return;
    }
    this.onSubmit(submitData).then(
      () => {
        this.routing.push(this.listUrl);
        Notify.success(this.successText);
      },
      (err) => {
        if (!err || isEmpty(err)) {
          return;
        }
        const { response: { data: responseData } = {} } = err || {};
        const { forbidden: { message = '' } = {} } = responseData || {};
        if (
          message &&
          isString(message) &&
          message.includes('Quota exceeded')
        ) {
          Notify.error(t('Quota exceeded'));
        } else {
          Notify.errorWithDetail(responseData, this.errorText);
        }
      }
    );
  };
}

export default inject('rootStore')(observer(StepCreate));
