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
          vim.keymap.set({ 'i', 'n', 'x' }, '<F36>', function()
            vim.fn.setreg('*', vim.fn.join(vim.api.nvim_buf_get_lines(0, 0, -1, true), '\n'))
            vim.bo.undolevels = vim.bo.undolevels -- undo-break を実行
            vim.api.nvim_buf_set_lines(0, 0, -1, true, {})
            vim.fn['skkeleton#handle']('enable', {})

            if vim.api.nvim_get_mode().mode == 'i' then
              return
            end
            vim.api.nvim_input('<Esc>i')
          end)

          vim.api.nvim_create_autocmd({ 'User' }, {
            pattern = { 'DenopsPluginPost:skkeleton' },
            callback = function()
              vim.api.nvim_input('i')
              vim.fn['skkeleton#handle']('enable', {})
            end,
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

launch()

!@:: {
  global nimeHwnd

  isActive := winActive(createCriteria())

  launch()

  if (isActive) {
    send('^{F12}')
    winHide(createCriteria())
    send('!{Esc}')
  } else {
    winShow(createCriteria())
    winActivate(createCriteria())
  }

  return
}

oe(reason, code) {
  if (not nimeHwnd) {
    return
  }
  try {
    winClose(createCriteria())
  }
}
onExit(oe)
