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

import { action } from 'mobx';
import client from 'client';
import Base from 'stores/base';

export class SubnetStore extends Base {
  get client() {
    return client.neutron.subnets;
  }

  get listFilterByProject() {
    return false;
  }

  @action
  async update({ id }, values) {
    const {
      host_routes,
      allocation_pools,
      project_id,
      subnet_name,
      enable_dhcp,
      gateway_ip,
      dns_nameservers,
    } = values;
    const data = {
      project_id,
      name: subnet_name,
      enable_dhcp,
      dns_nameservers,
      allocation_pools,
      host_routes,
      gateway_ip,
    };
    return this.submitting(this.client.update(id, { subnet: data }));
  }
}

const globalSubnetStore = new SubnetStore();
export default globalSubnetStore;
