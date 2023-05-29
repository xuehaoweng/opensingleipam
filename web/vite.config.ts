import vue from '@vitejs/plugin-vue'
import viteSvgIcons from 'vite-plugin-svg-icons'
// @ts-ignore
import path from 'path'
import {loadEnv} from 'vite'
import vitePluginCompression from 'vite-plugin-compression'
import ViteComponents from 'unplugin-vue-components/vite'
import {NaiveUiResolver} from 'unplugin-vue-components/resolvers'
import vueJsx from '@vitejs/plugin-vue-jsx'

// @ts-ignore
export default ({mode}) => {
    const env = loadEnv(mode, './')
    const config = {
        plugins: [
            vue(),
            viteSvgIcons({
                iconDirs: [path.resolve(process.cwd(), 'src/icons')],
                symbolId: 'icon-[dir]-[name]',
            }),
            vitePluginCompression({
                threshold: 1024 * 10,
            }),
            ViteComponents({
                resolvers: [NaiveUiResolver()],
            }),
            vueJsx(),
        ],
        resolve: {
            alias: [
                {
                    find: '@/',
                    replacement: path.resolve(process.cwd(), 'src') + '/',
                },
            ],
        }, build: {
            sourcemap: false,
            minify: 'terser',
            chunkSizeWarningLimit: 1500,
            terserOptions: {
                compress: {
                    drop_console: true,
                    drop_debugger: true
                }
            },
            rollupOptions: {
                output: {
                    manualChunks(id) {
                        if (id.includes('node_modules')) {
                            return id
                                .toString()
                                .split('node_modules/')[1]
                                .split('/')[0]
                                .toString();
                        }
                    },
                    chunkFileNames: (chunkInfo) => {
                        const facadeModuleId = chunkInfo.facadeModuleId
                            ? chunkInfo.facadeModuleId.split('/')
                            : [];
                        const fileName =
                            facadeModuleId[facadeModuleId.length - 2] || '[name]';
                        return `js/${fileName}/[name].[hash].js`;
                    }
                }
            }
        },
        server: {
            // hmr:{
            //   overlay:false
            // },
            open: true,
            proxy: {
                '/ipam': {
                    target: env.VITE_BASIC_URL,
                    ws: true, //代理websockets
                    changeOrigin: true, // 虚拟的站点需要更管origin
                    rewrite: (path: string) => path.replace(/^\/ipam/, '/ipam'),
                },
                '/rbac': {
                    target: env.VITE_BASIC_RBAC,
                    // ws: true, //代理websockets
                    changeOrigin: true, // 虚拟的站点需要更管origin
                    rewrite: (path: string) => path.replace(/^\/rbac/, '/rbac'),
                },
                '/ws': {
                    target: env.VITE_BASIC_URL,
                    timeout: 60000,
                    ws: true, //代理websockets
                    changeOrigin: true, // 虚拟的站点需要更管origin
                    rewrite: (path: string) => path.replace(/^\/ws/, '/ws'),
                },


            },
        },
    }
    if (mode === 'staging') {
        return Object.assign(
            {
                base: '/admin-work/',
            },
            config
        )
    } else {
        return Object.assign(
            {
                base: '/',
            },
            config
        )
    }
}
