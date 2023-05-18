import { FormItem } from './../../types/components'
import { defineComponent, h, PropType, ref, toRef } from 'vue'
import { FormProps, NForm, NFormItem, NFormItemGridItem, NGrid, useMessage } from 'naive-ui'
import service from '@/api/axios.config'

function renderItem(formItem: FormItem) {
  return function() {
    if (formItem.render) {
      return formItem.required
          ? [
            formItem.render(formItem),
            h(
                'span',
                {
                  class: 'ml-2 text-red-800 align-top',
                },
                '*',
            ),
          ]
          : formItem.render(formItem)
    } else {
      return ''
    }
  }
}

export default defineComponent({
  name: 'DataForm',
  props: {
    formConfig: {
      type: Object as PropType<FormProps>,
      default: () => {
      },
    },
    preset: {
      type: String,
      default: 'form-item',
      validator: (value: string) => {
        if (!['form-item', 'grid-item', 'grid-two-item'].includes(value)) {
          console.error(
              'preset value must be `form-item` or `grid-item` or `grid-two-item`, the default value is `form-item`',
          )
          return false
        }
        return true
      },
    },
    options: {
      type: Array as PropType<Array<FormItem>>,
      require: true,
    },
  },
  setup(props) {
    const dataForm = ref<typeof NForm | null>(null)
    const options = toRef(props, 'options')
    const message = useMessage()

    function reset() {
      if (!options.value) return
      options.value.forEach((it: FormItem) => {
        if (it.reset) {
          it.reset(it)
        } else {
          it.value.value = ''
        }
      })
    }

    function generatorParams() {
      if (!options.value) return
      return options.value.reduce((pre: any, cur: FormItem) => {
        pre[cur.key] = cur.value.value
        return pre
      }, {})
    }

    function validator() {
      if (!options.value) return
      return options.value.every((it: FormItem) => {
        if (it.required) {
          if (it.validator) {
            return it.validator(it, message)
          }
          if (it.value.value) {
            return true
          }
          message.error(it.label + '不能为空')
          return false
        }
        return true
      })
    }

    return {
      dataForm,
      reset,
      validator,
      generatorParams,
    }
  },
  render() {
    if (!this.options) {
      throw new Error('prop options must be not null')
    }
    return h(
        NForm,
        {
          ref: 'dataForm',
          labelPlacement: 'left',
          size: 'small',
          ...this.formConfig,
          // style: { height: '600px' },
        },
        {
          default: () => {
            return this.preset === 'grid-item'
                ?
                h(
                    NGrid,
                    {
                      responsive: 'screen',
                      cols: '4',
                      xGap: 5,
                    },
                    {
                      default: () => {
                        return this.options?.map((it) => {
                          return h(
                              NFormItemGridItem,
                              {
                                label: it.label,
                              },
                              {
                                default: renderItem(it),
                              },
                          )
                        })
                      },
                    },
                )
                : (this.preset === 'grid-two-item' ? h(
                    NGrid,
                    {
                      responsive: 'screen',
                      cols: '2',
                      xGap: 5,
                    },
                    {
                      default: () => {
                        return this.options?.map((it) => {
                          return h(
                              NFormItemGridItem,
                              {
                                label: it.label,
                              },
                              {
                                default: renderItem(it),
                              },
                          )
                        })
                      },
                    },
                    )
                    :
                    this.options?.map((it) => {
                      return h(
                          NFormItem,
                          {
                            label: it.label,
                            path: it.path || (it.key as string),
                          },
                          {
                            default: renderItem(it),
                          },
                      )
                    }))
          },
        },
    )
  },
})
