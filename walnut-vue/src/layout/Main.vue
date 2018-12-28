<template>
  <div id="main">
    <el-col :span="24">
      <el-tabs type="border-card">
        <el-tab-pane label="Vpn时长统计">
          <vpntable></vpntable>
        </el-tab-pane>
        <el-tab-pane label="重制密码">
          <modifypassword></modifypassword>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </div>
</template>

<script>
import VpnTable from '@/components/VpnTable'
import Modifypassword from '@/components/ModifyPassword'
export default {
  name: 'Main',
  components: {
    vpntable: VpnTable,
    modifypassword: Modifypassword
  }
}
</script>
