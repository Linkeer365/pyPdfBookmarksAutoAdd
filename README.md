# pyPdfBookmarksAutoAdd
Auto addition bookmarks to pdfs.

- 这个版本极度僵硬, 极度鸡肋, 可以嘲讽批评, 不要使用,

- 现在的问题是:
  - 现在已经抛弃OCR这个弟弟玩意了
    - <del>OCR后可能出现几种情况
    - 1. 原pdf文件空行ocr后还是空行, 这个无视
    - 2. 原pdf文件不是空行, 但是ocr是空行, 这个可以通过getCataIndices慢慢修改
    - 3. 元pdf文件的一些装饰字符, 被OCR进来变成一行, 凭空多了一行, 这个没法解决, 用getCataIndices也不太好改
    - 4. 原pdf文件的字符, 被错误的读取进来, 然后我们都没有意识到这个目录数字是有问题的 这个在getCataIndices里面很好改</del>
  - 已经证实, 只要先做完全部的addPage, 再进行addBookmarks就没有任何问题, 过去的书签会被全部移除, 具体见pyremovebookmarksCheck
    <del>没有移除书签的func在里面, 可能会产生书签冲撞, 现在还没有这个问题就是了<del>
  - 
  
  
