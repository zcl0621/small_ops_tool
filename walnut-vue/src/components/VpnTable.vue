<template>
  <div>
    <el-table
    :data="tableData"
    style="width: 100%"
    :default-sort = "{prop: 'id', order: 'descending'}"
    >
    <el-table-column
      prop="id"
      label="ID"
      sortable>
    </el-table-column>
    <el-table-column
      prop="cn_name"
      label="姓名"
      sortable>
    </el-table-column>
    <el-table-column
      prop="username"
      label="用户名"
      sortable>
    </el-table-column>
    <el-table-column
      prop="online"
      label="在线"
      sortable :sort-method="onlineSortby">
      <template slot-scope="scope">
      <i v-if="scope.row.online === true" class="el-icon-d-caret"></i>
      <i v-else class="el-icon-close"></i>
      </template>
    </el-table-column>
    <el-table-column
      prop="online_sum_time"
      label="在线时长"
      sortable
      :formatter="formatter">
    </el-table-column>
  </el-table>
  </div>
</template>

<script>
export default {
  name: 'VpnTable',
  data () {
    return {
      tableData: []
    }
  },
  methods: {
    formatter (row, column) {
      return Math.ceil(row.online_sum_time / 3600)
    },
    onlineSortby (row, column) {
      return (row.online && !column.online) ? -1 : 1
    }
  },
  mounted () {
    this.$http({
      methods: 'get',
      url: '/api/vpn/'
    }).then(response => {
      this.tableData = response.data.results
    }, function (error) {
      alert(error.response)
    })
  }
}
</script>
