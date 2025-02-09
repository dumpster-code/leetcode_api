local script_path = debug.getinfo(1, "S").source:sub(2)
local api_dir = script_path:gsub("/scripts/[^/]+$", "/")

local description_context = nil
local description_win = nil

local function display_description_window()
    print('display testing...' .. (description_context or "No description"))

    if description_win and vim.api.nvim_win_is_valid(description_win) then
        vim.api.nvim_win_close(description_win, true)
        description_win = nil
        return
    end

    local description_buf = vim.api.nvim_create_buf(false, true)     -- Create a new buffer
    vim.bo[description_buf].filetype = "markdown"
    vim.bo[description_buf].modifiable = true

    local lines = vim.split(description_context or "No description available", "\n")
    vim.api.nvim_buf_set_lines(description_buf, 0, -1, false, lines)

    local win_width = math.floor(vim.o.columns * 0.8)
    local win_height = math.floor(vim.o.lines * 0.8)
    local row = math.floor((vim.o.lines - win_height) / 2)
    local col = math.floor((vim.o.columns - win_width) / 2)

    description_win = vim.api.nvim_open_win(description_buf, true, {
        relative = "editor",
        width = win_width,
        height = win_height,
        row = row,
        col = col,
        style = "minimal",
        border = "rounded",
    })
end

local function display_problem(name, content, filetype)
    vim.cmd("enew")
    local buf = vim.api.nvim_get_current_buf()
    vim.api.nvim_buf_set_name(buf, name)

    if type(content) == "table" then
        content = vim.fn.json_encode(content)
    end

    if type(content) == "string" then
        content = vim.split(content, "\n")
    end

    vim.api.nvim_buf_set_lines(buf, 0, -1, false, content)
    vim.bo.filetype = filetype
end


local function run_python_script(path)
    path = api_dir .. path

    vim.fn.jobstart({ "python", path }, {
        stdout_buffered = true,
        on_stdout = function(_, data)
            if data and #data > 0 then
                local content = table.concat(data, "\n")

                vim.cmd("enew")
                local buf = vim.api.nvim_get_current_buf()

                local lines = vim.split(content, "\n")
                vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)

                vim.bo.filetype = "json"
            else
                print("No output from Python script.")
            end
        end,
        on_stderr = function(_, data)
            if data and #data > 0 then
                print("Python script error: " .. table.concat(data, "\n"))
            end
        end
    })
end

local function fetch_http(url, callback)
    vim.fn.jobstart({ "curl", "-s", url }, {
        stdout_buffered = true,
        on_stdout = function(_, data)
            if data and callback then
                local json_string = table.concat(data, "\n")
                local success, response = pcall(vim.fn.json_decode, json_string)
                print(response)

                if success then
                    callback(response)
                else
                    print("JSON decode error: " .. json_string)
                end
            end
        end
    })
end

local function get_daily_problem()
    local url = "http://127.0.0.1:8000/leetcode/daily"
    fetch_http(url, function(response)
        if not response then
            print("Invalid response from server")
            return
        end

        -- Display C++ Code Snippet
        if response.codeSnippets then
            local cpp_code = nil
            for _, snippet in ipairs(response.codeSnippets) do
                if snippet.langSlug == "cpp" then
                    cpp_code = snippet.code
                    break
                end
            end

            if cpp_code then
                display_problem("leetcode_solution.cpp", cpp_code, "cpp")
            else
                print("No C++ code snippet found")
            end
        end

        if response.content then
            -- Convert HTML to plain text (basic replacement)
            description_context = response.content
                :gsub("<[^>]+>", "") -- Remove HTML tags
                :gsub("&lt;", "<"):gsub("&gt;", ">"):gsub("&nbsp;", " ")

            print('display testing...' .. (description_context or "No description"))

            display_description_window()
        else
            print("No description found in response")
        end
    end)
end

require("which-key").add({
    { "<leader>l", group = "[L]eetCode", mode = { 'n' } }
})

vim.keymap.set("n", "<leader>ld", get_daily_problem, { desc = "[D]aily Problem" })
vim.keymap.set("n", "<leader>lz", display_description_window, { desc = "[O]pen Description" })

vim.keymap.set("n", "<leader>ls", ":wa | luafile " .. script_path .. "<CR>", { desc = "Write all and reload Lua file" })

-- run_python_script("scripts/problem_run.py")
