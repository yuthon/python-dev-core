"""ロギング機能のテスト"""

from __future__ import annotations

import logging
from unittest.mock import patch

import pytest

from python_dev_core.utils.logging import AutoLogMeta, instrument
from python_dev_core.utils.logging._logconfig import (
    _resolve_level,
    configure_root_logger,
)


class TestAutoLogging:
    """自動ロギング機能のテスト"""

    def test_auto_log_meta_class(self, caplog: pytest.LogCaptureFixture) -> None:
        """AutoLogMetaメタクラスのテスト"""
        caplog.set_level(logging.DEBUG)

        class TestClass(metaclass=AutoLogMeta):
            def test_method(self, x: int) -> int:
                return x * 2

        obj = TestClass()
        result = obj.test_method(5)

        assert result == 10
        assert len(caplog.records) == 2
        assert "test_method ⇢" in caplog.records[0].message
        assert "test_method ⇠" in caplog.records[1].message

    def test_instrument_function(self, caplog: pytest.LogCaptureFixture) -> None:
        """instrument関数のテスト"""
        caplog.set_level(logging.DEBUG)

        def simple_function(a: int, b: int) -> int:
            return a + b

        instrumented = instrument(simple_function)
        result = instrumented(3, 4)

        assert result == 7
        assert len(caplog.records) == 2
        assert "simple_function ⇢" in caplog.records[0].message
        assert "simple_function ⇠" in caplog.records[1].message

    def test_private_methods_not_instrumented(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """プライベートメソッドが計装されないことのテスト"""
        caplog.set_level(logging.DEBUG)

        class TestClass(metaclass=AutoLogMeta):
            def public_method(self) -> str:
                return self._private_method()

            def _private_method(self) -> str:
                return "private"

        obj = TestClass()
        result = obj.public_method()

        assert result == "private"
        # public_methodのログのみが記録される
        logged_methods = [r.message for r in caplog.records if "⇢" in r.message]
        assert len(logged_methods) == 1
        assert "public_method" in logged_methods[0]
        # プライベートメソッドのログが含まれていないことを確認
        all_messages = " ".join(r.message for r in caplog.records)
        assert "_private_method ⇢" not in all_messages

    def test_exception_handling(self, caplog: pytest.LogCaptureFixture) -> None:
        """例外発生時のログ出力テスト"""
        caplog.set_level(logging.DEBUG)

        class TestClass(metaclass=AutoLogMeta):
            def failing_method(self) -> None:
                raise ValueError("Test error")

        obj = TestClass()
        with pytest.raises(ValueError):
            obj.failing_method()

        # 例外発生時のログが記録される
        assert any("!! raised" in r.message for r in caplog.records)

    def test_log_level_filtering(self, caplog: pytest.LogCaptureFixture) -> None:
        """ログレベルによるフィルタリングのテスト"""
        caplog.set_level(logging.INFO)

        class TestClass(metaclass=AutoLogMeta):
            def test_method(self) -> str:
                return "result"

        obj = TestClass()
        result = obj.test_method()

        assert result == "result"
        # DEBUGレベルのログは記録されない
        assert len(caplog.records) == 0


class TestLogConfig:
    """ログ設定のテスト"""

    def test_log_level_from_env(self) -> None:
        """環境変数からログレベルを取得するテスト"""

        with patch.dict("os.environ", {"LOG_LEVEL": "WARNING"}):
            level = _resolve_level()
            assert level == logging.WARNING

    def test_default_log_level(self) -> None:
        """デフォルトログレベルのテスト"""

        with patch.dict("os.environ", {"LOG_LEVEL": ""}):
            level = _resolve_level()
            assert level == logging.INFO

    def test_configure_root_logger(self) -> None:
        """ルートロガー設定のテスト"""

        # 既存のハンドラをクリア
        root = logging.getLogger()
        root.handlers.clear()

        configure_root_logger()

        assert len(root.handlers) == 1
        assert isinstance(root.handlers[0], logging.StreamHandler)
        assert root.level == logging.INFO

        # 再度呼び出してもハンドラが重複しないことを確認
        configure_root_logger()
        assert len(root.handlers) == 1
