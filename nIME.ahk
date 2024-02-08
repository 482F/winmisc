DetectHiddenWindows true

isInitial := true
imePid := ''
createWindowTitle := () => 'ahk_pid ' . imePid

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
  global imePid

  if (imePid !== '' && processExist(imePid)) {
    return
  }

  cmd := util.array.join(
    [
      ; 'wt', '-w', 'ime', 'new-tab', '-p', 'Ubuntu',
      ; 'nvim',
      'goneovim',
      '-c',
      '"lua (function()`n'
      . "
        (
          vim.keymap.set({ 'i', 'n', 'x' }, '<C-F12>', function()
            vim.fn.setreg('*', vim.fn.join(vim.api.nvim_buf_get_lines(0, 0, -1, true), '\n'))
            vim.bo.undolevels = vim.bo.undolevels -- undo-break を実行
            vim.api.nvim_buf_set_lines(0, 0, -1, true, {})
            vim.fn['skkeleton#handle']('enable', {})

            if vim.api.nvim_get_mode().mode == 'i' then
              return
            end
            vim.api.nvim_input('<Esc>i')
          end)
          vim.api.nvim_input('i')
          vim.api.nvim_create_autocmd({ 'InsertEnter' }, {
            callback = function()
              vim.fn.input('press Enter') -- 起動直後に resize とかを呼ぶと変なことになるので待つ
              vim.cmd.GonvimResize('\'935x306\'')
              vim.cmd.GonvimWinpos(16, 16)
              vim.fn['skkeleton#handle']('enable', {})
            end,
            once = true
          })
        )"
      . '`nend)()"'
    ],
    ' '
  )
  run(cmd, , , &imePid)
  winTitle := createWindowTitle()
  if (not winWait(winTitle, , 1) || not winWaitActive(winTitle, , 1)) {
    throw Error('launch failed')
  }

  winSetTransparent(200, winTitle)
}

!@:: {
  global isInitial
  global imePid

  launch()

  if (not isInitial && winActive(createWindowTitle())) {
    send('^{F12}')
    winHide(createWindowTitle())
    send('!{Esc}')
  } else {
    winShow(createWindowTitle())
    winActivate(createWindowTitle())
  }

  isInitial := false
  return
}

oe(reason, code) {
  if (not imePid) {
    return
  }
  processClose(imePid)
}
onExit(oe)

