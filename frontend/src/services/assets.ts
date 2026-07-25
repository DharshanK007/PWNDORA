import api from '@/lib/axios'
import type { PagedResponse } from './employees'

export interface Asset {
  id: string
  name: string
  status: string
  ip_address?: string
  mac_address?: string
  location?: string
  department_id?: string
  firmware_version?: string
  asset_group?: string
  last_patch_date?: string
  last_seen?: string
}

export const assetsService = {
  getAssets: async (skip = 0, limit = 100): Promise<PagedResponse<Asset>> => {
    const { data } = await api.get(`/devices/?skip=${skip}&limit=${limit}`)
    return data
  },
  getAsset: async (id: string): Promise<Asset> => {
    const { data } = await api.get(`/devices/${id}`)
    return data
  }
}
