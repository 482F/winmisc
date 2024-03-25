DetectHiddenWindows true
SetTitleMatchMode 3

nimeWinTitle := 'nime'
nimeHwnd := ''
createCriteria := () => 'ahk_id ' . nimeHwnd

class stream {
  static start(arr) {
    return stream(arr)
  }
  __New(arr) {
    this.arr := arr
  }
  map(func) {
    newarr := []
    for value in this.arr {
      newarr.push(func(value))
    }
    return stream(newarr)
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
        stream
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

launch() {
  global nimeHwnd

  if (nimeHwnd !== '' && winExist(createCriteria())) {
    return
  }

  cmd := util.array.join(
    [
      'wt',
      '-w', nimeWinTitle,
      '--pos', '16,16',
      '--size', '84,12',
      'new-tab',
      '--title', nimeWinTitle,
      'wsl', 'nvim', '-c', '"lua (function()`n'
      . "
        (
          local function finish_input()
            local postprocess = function()
              vim.fn.setreg('*', vim.fn.join(vim.api.nvim_buf_get_lines(0, 0, -1, true), '\n'))
              vim.bo.undolevels = vim.bo.undolevels -- undo-break を実行
              vim.api.nvim_buf_set_lines(0, 0, -1, true, {})
              vim.fn['skkeleton#handle']('enable', {})

              if vim.api.nvim_get_mode().mode == 'i' then
                return
              end
              vim.api.nvim_input('<Esc>i')
            end

            if vim.api.nvim_get_mode().mode == 'i' then
              vim.api.nvim_create_autocmd({ 'User' }, {
                pattern = { 'skkeleton-handled' },
                once = true,
                callback = postprocess,
              })
              vim.fn['skkeleton#handle']('disable', {})
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

  if (not winWait(nimeWinTitle, , 3)) {
    throw Error('launch failed')
  }
  nimeHwnd := winGetId(nimeWinTitle)

  winSetTransparent(200, createCriteria())
}

!@:: {
  global nimeHwnd

  isActive := winActive(createCriteria())

  launch()

  if (isActive) {
    A_Clipboard := ''
    send('^{F12}')
    clipWait(3)
    winHide(createCriteria())
    send('!{Esc}')
  } else {
    winShow(createCriteria())
    winActivate(createCriteria())
  }

  return
}

launch()

oe(reason, code) {
  if (not nimeHwnd) {
    return
  }
  try {
    winClose(createCriteria())
  }
}
onExit(oe)

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
+vkf2::F8
#HotIf

