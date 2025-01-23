<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartContainer = ref(null)
let chart = null

const initChart = () => {
  if (chart) {
    chart.dispose()
  }
  
  chart = echarts.init(chartContainer.value)
  updateChart()
}

const updateChart = () => {
  const option = {
    title: {
      text: '新闻真实性分析',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: Object.keys(props.data.factors || {})
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '可信度',
        type: 'bar',
        data: Object.values(props.data.factors || {}).map(v => (v * 100).toFixed(2)),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        }
      }
    ]
  }

  chart.setOption(option)
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => {
    chart && chart.resize()
  })
})

watch(() => props.data, () => {
  updateChart()
}, { deep: true })
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style> 