<template>
    <div>
       <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 ovferflow-hidden">
            <div>
                <h2 class="text-3xl font-bold text-white">数据分析仪表板</h2>
                <p class="text-gray-400 mt-1">欢迎回来，这是今天的数据概览。</p>
            </div>
            <div class="flex items-center space-x-2 mt-4 md:mt-0">
                <div class="relative">
                    <input type="text" placeholder="搜索航班或平台..." class="bg-gray-800 border border-gray-700 rounded-lg py-2 px-4 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-auto">
                    <svg class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /></svg>
                </div>
                <button @click="handtabinfo('capacity')" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg flex items-center transition-colors">
                    <svg class="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                    运输需求录入
                </button>
                <button @click="handtabinfo('airfreighter')" class="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center transition-colors">
                    <svg class="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.096 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    飞机信息修改
                </button>
                <button @click="handtabinfo('platform')" class="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center transition-colors">
                    <svg class="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.096 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    平台信息修改
                </button>
            </div>
        </header>

        <!-- Key Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-400 text-sm font-medium">当月飞行架次</p>
                        <p class="text-3xl font-bold text-white mt-2">1,280</p>
                    </div>
                    <div class="bg-blue-500/20 text-blue-400 p-2 rounded-lg">
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
                    </div>
                </div>
                    <p class="text-xs text-green-400 mt-4 flex items-center"><svg class="h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 17a.75.75 0 01-.75-.75V5.612L6.22 8.77a.75.75 0 01-1.06-1.06l4.25-4.25a.75.75 0 011.06 0l4.25 4.25a.75.75 0 01-1.06 1.06L10.75 5.612V16.25A.75.75 0 0110 17z" clip-rule="evenodd"/></svg> 5.2% vs 上月</p>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-400 text-sm font-medium">当月运输人数</p>
                        <p class="text-3xl font-bold text-white mt-2">15,342</p>
                    </div>
                        <div class="bg-green-500/20 text-green-400 p-2 rounded-lg">
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    </div>
                </div>
                    <p class="text-xs text-green-400 mt-4 flex items-center"><svg class="h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 17a.75.75 0 01-.75-.75V5.612L6.22 8.77a.75.75 0 01-1.06-1.06l4.25-4.25a.75.75 0 011.06 0l4.25 4.25a.75.75 0 01-1.06 1.06L10.75 5.612V16.25A.75.75 0 0110 17z" clip-rule="evenodd"/></svg> 8.1% vs 上月</p>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-400 text-sm font-medium">平均飞行成本</p>
                        <p class="text-3xl font-bold text-white mt-2">¥ 35,400</p>
                    </div>
                        <div class="bg-yellow-500/20 text-yellow-400 p-2 rounded-lg">
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v.01" /></svg>
                    </div>
                </div>
                <p class="text-xs text-red-400 mt-4 flex items-center"><svg class="h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a.75.75 0 01.75.75v10.388l3.03-3.03a.75.75 0 111.06 1.06l-4.25 4.25a.75.75 0 01-1.06 0l-4.25-4.25a.75.75 0 111.06-1.06l3.03 3.03V3.75A.75.75 0 0110 3z" clip-rule="evenodd" /></svg> 1.5% vs 上月</p>
            </div>
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-400 text-sm font-medium">准点率</p>
                        <p class="text-3xl font-bold text-white mt-2">98.6%</p>
                    </div>
                    <div class="bg-purple-500/20 text-purple-400 p-2 rounded-lg">
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </div>
                </div>
                <p class="text-xs text-gray-400 mt-4 flex items-center">与上月持平</p>
            </div>
        </div>
    </div> 
</template>

<script setup>
import { useEventCentre } from '@/hooks/useEventCentre'
const props = defineProps({
  propValue: {
    type: Object,
    default: () => ({
    })
  },
  element: {
    type: Object,
    default: () => ({})
  }
})

const { onClickOther } = useEventCentre();
const handtabinfo = (info) => {
    let selectTabKey = info
    console.log('点击了运输需求录入', info);
    onClickOther({element: props.element, clickName: 'handtabinfo', params: { selectTabKey }})
}
</script>
