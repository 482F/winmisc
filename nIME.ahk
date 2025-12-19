DetectHiddenWindows true
SetTitleMatchMode 2 ; 部分一致

class nime {
  static winTitle := 'nime'
  static hwnd := ''
  static createCriteria() {
    return 'ahk_id ' . nime.hwnd
  }
  class stream {
    static start(arr) {
      return nime.stream(arr)
    }
    __New(arr) {
      this.arr := arr
    }
    map(func) {
      newarr := []
      for value in this.arr {
        newarr.push(func(value))
      }
      return nime.stream(newarr)
    }
    reduce(func, initial) {
      result := initial
      for value in this.arr {
        result := func(result, value)
      }
      return result
    }
    collect() {
      return this.arr
    }
  }

  class util {
    class array {
      static join(arr, separator) {
        return substr(
          nime.stream
            .start(arr)
            .reduce((all, part) => all . separator . part, ''),
          2
        )
      }
    }
    class string {
      static wrap(str, wrapper) {
        return wrapper . str . wrapper
      }
    }
  }
  static launch() {
    if (nime.hwnd !== '' && winExist(nime.createCriteria())) {
      return
    }

    cmd := nime.util.array.join(
      [
        'wt',
        '-w', nime.winTitle,
        '--pos', '120,16',
        '--size', '84,12',
        'new-tab',
        '--title', nime.winTitle,
        'wsl', 'nvim', '-c', '"lua (function()`n'
        . "
          (
            local function postprocess()
              vim.fn.setreg('*', vim.fn.join(vim.api.nvim_buf_get_lines(0, 0, -1, true), '\n'))
              vim.bo.undolevels = vim.bo.undolevels -- undo-break を実行
              vim.api.nvim_buf_set_lines(0, 0, -1, true, {})

              vim.api.nvim_input('i')
              vim.fn['skkeleton#handle']('enable', {})
            end

            local function finish_input()
              vim.api.nvim_input('<Esc><Esc>')
              if vim.fn['skkeleton#is_enabled']() then
                vim.api.nvim_create_autocmd({ 'User' }, {
                  pattern = { 'skkeleton-handled' },
                  once = true,
                  callback = postprocess,
                })
              else
                postprocess()
              end
            end

            local function init()
              vim.api.nvim_input('i')
              vim.fn['skkeleton#handle']('enable', {})

              vim.keymap.set({ 'i', 'n', 'x' }, '<F36>', finish_input)
            end

            vim.api.nvim_create_autocmd({ 'User' }, {
              pattern = { 'DenopsPluginPost:skkeleton' },
              callback = init,
            })

          )"
        . '`nend)()"'
      ],
      ' '
    )
    run(cmd)

    if (not winWait(nime.winTitle, , 10)) {
      throw Error('launch failed')
    }
    nime.hwnd := winGetId(nime.winTitle)

    winSetTransparent(200, nime.createCriteria())
  }
  static oe(reason, code) {
    if (not nime.hwnd) {
      return
    }
    try {
      winClose(nime.createCriteria())
    }
  }
}


!@:: {
  isActive := winActive(nime.createCriteria())

  nime.launch()

  if (isActive) {
    A_Clipboard := ''
    send('^{F12}')
    clipWait(3)
    winHide(nime.createCriteria())
    send('!{Esc}')
  } else {
    winShow(nime.createCriteria())
    winActivate(nime.createCriteria())
  }

  return
}

onExit((args*) => nime.oe(args*))

; 全角半角キーを無効化
vkF3::return
vkF4::return

#HotIf WinActive('ahk_exe WindowsTerminal.exe') WinActive('ahk_exe nvim-qt.exe')
; CapsLock、無変換、変換、かなキーをリマップ
vkf0::F1
vk1d::F2
vk1c::F3
vkf2::F4
+vkf0::F5
+vk1d::F6
+vk1c::F7
+vkf1::F8
#HotIf

