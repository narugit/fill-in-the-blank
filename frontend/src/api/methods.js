import Api from './index'

export default {
  testPosting(input_data) {
    const item = { data: input_data }
    return Api().post('/test', item)
  }
  // 他の処理も追加可能
}
