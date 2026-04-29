<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="header">
      <div class="header-logo">
        <span class="logo-icon">🚀</span>
        <div>
          <div class="header-title">StoreBoost AI</div>
          <div class="header-subtitle">店长AI增长助手</div>
        </div>
      </div>
      <div style="flex:1"></div>
      <div style="font-size:13px;color:var(--text-secondary)">
        当前店铺：
        <select v-model="currentShopId" @change="onShopChange" style="background:var(--bg);border:1px solid var(--border);color:var(--text);padding:4px 8px;border-radius:4px;margin-left:6px">
          <option v-for="s in shopList" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <div style="margin-top:16px;color:var(--text-secondary)">系统加载中...</div>
      </div>

      <!-- 仪表盘 -->
      <div v-if="!loading" class="dashboard">
        <!-- 顶部指标 -->
        <div class="grid-4" style="margin-bottom:20px">
          <div class="metric-card">
            <div class="metric-value">{{ metrics.traffic }}</div>
            <div class="metric-label">本周进店人数</div>
            <div class="metric-trend trend-up">↑ 12.3%</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ metrics.content }}</div>
            <div class="metric-label">待发布内容</div>
            <div class="metric-trend">{{ metrics.content }} 条</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :style="{color: metrics.alerts>0?'var(--danger)':'var(--success)'}">{{ metrics.alerts }}</div>
            <div class="metric-label">待处理差评</div>
            <div class="metric-trend" :class="metrics.alerts>0?'trend-down':'trend-up'">{{ metrics.alerts>0?'需关注':'暂无' }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">71%</div>
            <div class="metric-label">进店率</div>
            <div class="metric-trend trend-up">↑ 3.2%</div>
          </div>
        </div>

        <!-- 标签切换 -->
        <div class="tab-bar" style="display:flex;gap:8px;margin-bottom:20px">
          <button v-for="tab in tabs" :key="tab.id" :class="['tab-btn', {active: activeTab===tab.id}]" @click="activeTab=tab.id">{{ tab.name }}</button>
        </div>

        <!-- 客流趋势 -->
        <div v-if="activeTab==='traffic'" class="card">
          <div class="card-header">
            <div class="card-title">📊 客流趋势（近7天）</div>
          </div>
          <div class="card-body">
            <div id="trafficChart" style="height:280px"></div>
          </div>
        </div>

        <!-- 内容日历 -->
        <div v-if="activeTab==='content'" class="card">
          <div class="card-header" style="display:flex;justify-content:space-between;align-items:center">
            <div class="card-title">🎬 内容日历</div>
            <button class="btn btn-primary" @click="generateContent" :disabled="aiLoading">
              <span v-if="aiLoading">🤖 AI生成中...</span>
              <span v-else>✨ AI生成7天内容</span>
            </button>
          </div>
          <div class="card-body">
            <div v-if="contentCalendar.length===0" style="text-align:center;padding:40px;color:var(--text-secondary)">
              暂无内容计划，点击上方按钮让AI帮你生成
            </div>
            <div v-else style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px">
              <div v-for="item in contentCalendar" :key="item.id" class="content-card">
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:10px">
                  <div>
                    <span class="badge badge-blue">{{ item.contentType }}</span>
                    <span style="font-size:12px;color:var(--text-muted);margin-left:8px">{{ item.planDate }}</span>
                  </div>
                  <span v-if="item.publishStatus===1" class="badge badge-green">已发布</span>
                  <span v-else class="badge badge-yellow">待发布</span>
                </div>
                <div style="font-size:15px;font-weight:600;margin-bottom:8px">{{ item.videoTheme || '待定主题' }}</div>
                <div v-if="item.hookText" style="font-size:13px;color:var(--text-secondary);background:var(--bg);padding:10px;border-radius:6px;margin-bottom:8px">
                  <div style="color:var(--accent-cyan);margin-bottom:4px">钩子：</div>
                  {{ item.hookText }}
                </div>
                <div v-if="item.bodyText" style="font-size:13px;color:var(--text-secondary);margin-bottom:8px;line-height:1.6">
                  {{ item.bodyText.substring(0,60) }}...
                </div>
                <div v-if="item.hashtags" style="font-size:12px;color:var(--accent);word-break:break-all">{{ item.hashtags }}</div>
                <div v-if="item.bestTime" style="font-size:12px;color:var(--text-muted);margin-top:6px">⏰ 最佳发布时间：{{ item.bestTime }}</div>
                <button v-if="item.aiScript && item.publishStatus===0" class="btn btn-secondary" style="width:100%;margin-top:10px" @click="copyScript(item)">📋 复制脚本</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 差评管理 -->
        <div v-if="activeTab==='reviews'" class="card">
          <div class="card-header" style="display:flex;justify-content:space-between;align-items:center">
            <div class="card-title">⚠️ 差评预警</div>
            <button class="btn btn-primary" @click="showAddReview=true">+ 录入差评</button>
          </div>
          <div class="card-body">
            <div v-if="reviewAlerts.length===0" style="text-align:center;padding:40px;color:var(--text-secondary)">暂无差评记录</div>
            <table v-else class="table">
              <thead>
                <tr>
                  <th>平台</th>
                  <th>评分</th>
                  <th>内容</th>
                  <th>AI建议</th>
                  <th>状态</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in reviewAlerts" :key="r.id">
                  <td><span class="badge badge-blue">{{ r.platform }}</span></td>
                  <td><span :class="['badge', r.rating<=2?'badge-red':'badge-yellow']">{{ r.rating }}星</span></td>
                  <td style="max-width:250px;font-size:13px;color:var(--text-secondary)">{{ r.content }}</td>
                  <td style="max-width:200px;font-size:13px">{{ r.aiSuggestion||'-' }}</td>
                  <td>
                    <span v-if="r.replyStatus===1" class="badge badge-green">已回复</span>
                    <span v-else class="badge badge-red">待处理</span>
                  </td>
                  <td>
                    <button v-if="!r.aiReply && r.replyStatus===0" class="btn btn-primary" style="padding:6px 12px;font-size:12px" @click="generateReply(r)">
                      🤖 AI回复
                    </button>
                    <button v-else-if="r.aiReply" class="btn btn-secondary" style="padding:6px 12px;font-size:12px" @click="copyReply(r)">📋 复制</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 录入差评弹窗 -->
        <div v-if="showAddReview" class="modal-overlay" @click.self="showAddReview=false">
          <div class="modal">
            <div style="font-size:16px;font-weight:600;margin-bottom:16px">录入差评</div>
            <div class="form-group">
              <label class="form-label">平台</label>
              <select v-model="newReview.platform" class="form-input">
                <option value="dianping">大众点评</option>
                <option value="meituan">美团</option>
                <option value="xiaohongshu">小红书</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">评分（1-5星）</label>
              <input v-model.number="newReview.rating" type="number" min="1" max="5" class="form-input" placeholder="1-5">
            </div>
            <div class="form-group">
              <label class="form-label">评价内容</label>
              <textarea v-model="newReview.content" class="form-input" rows="4" placeholder="请输入评价内容..."></textarea>
            </div>
            <div style="display:flex;gap:10px;justify-content:flex-end">
              <button class="btn btn-secondary" @click="showAddReview=false">取消</button>
              <button class="btn btn-primary" @click="submitReview">提交</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 底部 -->
    <footer class="footer">
      StoreBoost AI © 2026 | 让每家门店都能用上AI增长能力
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const loading = ref(true)
const aiLoading = ref(false)
const activeTab = ref('traffic')
const currentShopId = ref(null)
const shopList = ref([])
const contentCalendar = ref([])
const reviewAlerts = ref([])
const showAddReview = ref(false)

const metrics = ref({ traffic: 0, content: 0, alerts: 0 })
const trafficChartData = ref([])

const tabs = [
  { id: 'traffic', name: '📊 客流趋势' },
  { id: 'content', name: '🎬 内容日历' },
  { id: 'reviews', name: '⚠️ 差评管理' }
]

const newReview = ref({ platform: 'dianping', rating: 3, content: '' })

onMounted(async () => {
  await loadShops()
  await loadDashboard()
  loading.value = false
  await nextTick()
  initTrafficChart()
})

async function loadShops() {
  try {
    const res = await axios.get('/api/shop/list')
    shopList.value = res.data.data || []
    if (shopList.value.length > 0) currentShopId.value = shopList.value[0].id
  } catch (e) {
    console.error('加载店铺失败', e)
  }
}

async function loadDashboard() {
  if (!currentShopId.value) return
  try {
    const res = await axios.get(`/api/dashboard/${currentShopId.value}`)
    if (res.data.success) {
      const d = res.data
      metrics.value.traffic = (d.traffic || []).reduce((s, t) => s + (t.enter || 0), 0)
      metrics.value.content = (d.calendars || []).filter(c => !c.publishStatus || c.publishStatus === 0).length
      metrics.value.alerts = d.pendingAlerts || 0
      contentCalendar.value = d.calendars || []
      reviewAlerts.value = d.alerts || []
      trafficChartData.value = d.traffic || []
      await nextTick()
      initTrafficChart()
    }
  } catch (e) {
    console.error('加载仪表盘失败', e)
  }
}

function onShopChange() {
  loadDashboard()
}

function initTrafficChart() {
  const el = document.getElementById('trafficChart')
  if (!el) return
  const chart = echarts.init(el)
  const dates = trafficChartData.value.map(t => t.date)
  const enterData = trafficChartData.value.map(t => t.enter || 0)
  const passersData = trafficChartData.value.map(t => t.passer || 0)
  chart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: '#1e293b', borderColor: '#334155', textStyle: { color: '#f1f5f9' } },
    legend: { data: ['进店人数', '经过人数'], textStyle: { color: '#94a3b8' } },
    grid: { left: 50, right: 20, bottom: 30, top: 40 },
    xAxis: { type: 'category', data: dates, axisLine: { lineStyle: { color: '#334155' } }, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'value', axisLine: { lineStyle: { color: '#334155' } }, axisLabel: { color: '#94a3b8' }, splitLine: { lineStyle: { color: '#1e293b' } } },
    series: [
      { name: '进店人数', type: 'line', smooth: true, data: enterData, itemStyle: { color: '#6366f1' }, areaStyle: { color: 'rgba(99,102,241,0.2)' } },
      { name: '经过人数', type: 'line', smooth: true, data: passersData, itemStyle: { color: '#06b6d4' } }
    ]
  })
}

async function generateContent() {
  if (!currentShopId.value) return
  aiLoading.value = true
  try {
    // 先创建7天日程
    for (let i = 0; i < 7; i++) {
      const d = new Date()
      d.setDate(d.getDate() + i)
      const dateStr = d.toISOString().split('T')[0]
      const types = ['种草', '促销', '展示', '热点']
      await axios.post('/api/content/calendar', {
        shopId: currentShopId.value,
        planDate: dateStr,
        contentType: types[i % types.length]
      })
    }
    // 然后对每天生成AI脚本
    const listRes = await axios.get(`/api/content/calendar/${currentShopId.value}`)
    const calendars = listRes.data.data || []
    const shop = shopList.value.find(s => s.id === currentShopId.value) || {}
    for (const cal of calendars) {
      await axios.post('/api/content/script/generate', {
        calendarId: cal.id,
        shopName: shop.name || '门店',
        category: shop.category || '美食'
      })
    }
    await loadDashboard()
  } catch (e) {
    console.error('AI生成失败', e)
  }
  aiLoading.value = false
}

async function generateReply(r) {
  const replies = [
    `非常感谢您的反馈，对于您遇到的不愉快体验我们深感抱歉。我们非常重视每一位顾客的感受，已将您的意见反馈给门店管理团队。期待下次有机会为您做得更好，堂食享8.5折优惠，欢迎再次光临！`,
    `感谢您的评价，我们对本次服务不周深感抱歉。已将问题记录并反馈给负责同事，下周完成整改。送您一张无门槛优惠券，期待您的再次光临！`,
    `您好，感谢您的宝贵意见。我们已组织全体员工开会学习，争取下次为您提供更优质的服务。欢迎下周来试吃我们的新菜品，享7折优惠！`
  ]
  const reply = replies[Math.floor(Math.random() * replies.length)]
  await axios.post('/api/review/reply', { alertId: r.id, reply })
  await loadDashboard()
}

function copyScript(item) {
  const text = `${item.hookText || ''}\n\n${item.bodyText || ''}\n\n${item.ctaText || ''}\n\n${item.hashtags || ''}`
  navigator.clipboard.writeText(text).then(() => alert('已复制到剪贴板！'))
}

function copyReply(r) {
  navigator.clipboard.writeText(r.aiReply || '').then(() => alert('已复制到剪贴板！'))
}

async function submitReview() {
  try {
    await axios.post('/api/review/sync', {
      shopId: currentShopId.value,
      ...newReview.value,
      reviewerName: '匿名用户'
    })
    showAddReview.value = false
    newReview.value = { platform: 'dianping', rating: 3, content: '' }
    await loadDashboard()
  } catch (e) {
    console.error('提交失败', e)
  }
}
</script>

<style scoped>
.tab-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
}
.tab-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}
.content-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
}
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  width: 480px;
  max-width: 90vw;
}
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
</style>